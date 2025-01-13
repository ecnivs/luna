# Response Handler
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from llm_handler import LlmHandler
from settings import *
import hashlib
import random

class ResponseHandler:
    def __init__(self):
        self.handler = LlmHandler()
        self.cache_file = CACHE_FILE
        self.cache = self.load_cache()
        self.stemmer = PorterStemmer()

    def hash_query(self, query):
        return hashlib.sha256(query.encode()).hexdigest()

    def load_cache(self):
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w') as file:
                json.dump({}, file)
            return {}
        else:
            with open(self.cache_file, 'r') as file:
                return json.load(file)

    def save_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)

    def extract_key_phrases(self, query):
        stop_words = set(stopwords.words('english'))
        words = re.sub(r'[^a-zA-Z\s]', '', query.lower()).split()
        word_counts = Counter([self.stemmer.stem(word) for word in words if word not in stop_words])
        result = list(word_counts.keys())
        if not result:
            return query.split()
        if result and result[0] in EXCLUDED_PREFIXES:
            result.pop(0)
        return result

    def add_response(self, query, query_hash, intent):
        response = self.handler.get_response(query).strip().lower()
        if response not in self.cache[intent]:
            self.cache[intent].append(response)
        self.cache[query_hash] = {
            'intent': intent
        }

    def handle(self, query):
        if query.lower().startswith("oh "):
            query = query[3:]
        query_hash = self.hash_query(query.lower())
        response = None

        if query_hash in self.cache:
            detected_intent = self.cache[query_hash]['intent']
            cached_responses = self.cache[detected_intent]
            if len(cached_responses) > 2:
                threading.Thread(target=self.add_response, args=(query, query_hash, detected_intent)).start()
                return f'{random.choice(cached_responses)}'

        response = self.handler.get_response(query).strip().lower()
        intent_name = '.'.join(self.extract_key_phrases(query))

        if 'repeat' not in intent_name:
            if intent_name not in self.cache:
                self.cache[intent_name] = []
            if response not in self.cache[intent_name]:
                self.cache[intent_name].append(response)
            self.cache[query_hash] = {
                'intent': intent_name
            }
        return response

