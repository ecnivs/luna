# response handler
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from llm_handler import LlmHandler
from dialogflow_handler import Agent
import hashlib
import json
import os
import random

class ResponseHandler:
    def __init__(self, core):
        self.handler = LlmHandler(core)
        self.agent = Agent('key.json', 'blossom-jwv9')
        self.cache_file = "cache.json"
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
        query = re.sub(r'[^a-zA-Z\s]', '', query.lower())
        words = query.split()
        filtered_words = [self.stemmer.stem(word) for word in words if word not in stop_words]
        word_counts = Counter(filtered_words)
        result = list(word_counts.keys())
        if result and result[0] == "tell":
            result.pop(0)
        return result

    def handle(self, query):
        query_hash = self.hash_query(query)
        agent_response = self.agent.get_response(query)
        response = None

        # check for timeout
        if agent_response is not None:
            if query_hash in self.cache:
                detected_intent = self.cache[query_hash]['intent']
                cached_responses = self.cache[detected_intent]
                if cached_responses:
                    return f'{random.choice(cached_responses)}'
            return self.handler.get_response(query)

        detected_intent = self.agent.detected_intent
        if not response:
            if detected_intent in ('web.search', 'Default Fallback Intent'):
                response = self.handler.get_response(query)
            else:
                response = self.agent.fulfillment_text

        # cache responses
        if detected_intent not in ('web.search', 'Default Fallback Intent'):
            if detected_intent not in self.cache:
                self.cache[detected_intent] = []

            if response not in self.cache[detected_intent]:
                self.cache[detected_intent].append(response)

            self.cache[query_hash] = {
                'intent': detected_intent
            }
        elif detected_intent == 'web.search':
            key_phrases = self.extract_key_phrases(query)
            intent_name = 'web.search.'+'.'.join(key_phrases)

            if intent_name not in self.cache:
                self.cache[intent_name] = []
            if response not in self.cache[intent_name]:
                self.cache[intent_name].append(response)
            self.cache[query_hash] = {
                'intent': intent_name
            }
        return response
