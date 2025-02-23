# Response Handler
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from llm_handler import LlmHandler
from settings import *
from cache_handler import LRUCache, LFUCache
import hashlib
import random

class ResponseHandler:
    def __init__(self, core):
        self.core = core
        self.lru_cache = LRUCache(MAX_LRU_SIZE)
        self.lfu_cache = LFUCache(MAX_LFU_SIZE)

        self.on_init()

    def on_init(self):
        self.llm = LlmHandler()
        self.cache = self.load_cache()
        self.stemmer = PorterStemmer()

    @staticmethod
    def hash_query(query):
        return hashlib.sha256(query.encode()).hexdigest()

    def load_cache(self):
        if not os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'w') as file:
                json.dump({'lru': {}, 'lfu': {}}, file)
            return

        with open(CACHE_FILE, 'r') as file:
            data = json.load(file)
            self.lru_cache.load(data.get('lru', {}))
            self.lfu_cache.load(data.get('lfu', {}))

    def save_cache(self):
        with open(CACHE_FILE, 'w') as file:
            json.dump({'lru': self.lru_cache.to_dict(), 'lfu': self.lfu_cache.to_dict()}, file)

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

    def fetch_and_store(self, query, query_hash, intent):
        new_response = []
        for chunk in self.llm.get_response(query):
            if chunk.strip():
                new_response.append(chunk)

        new_response = ' '.join(new_response)
        self.add_response(query, query_hash, intent, new_response)

    def add_response(self, query, query_hash, intent, response):
        existing_responses = self.lfu_cache.get(intent) or []

        if response not in existing_responses:
            existing_responses.append(response)
            self.lfu_cache.put(intent, existing_responses)

        self.lru_cache.put(query_hash, {'intent': intent})


    def handle(self, query):
        query_hash = self.hash_query(query.lower())
        cached_data = self.lru_cache.get(query_hash) or self.lfu_cache.get(query_hash)

        if cached_data:
            detected_intent = cached_data['intent']
            cached_responses = self.lfu_cache.get(detected_intent) or []

            if len(cached_responses) >= 2:
                last_used = self.lru_cache.get('last_used_response')
                possible_responses = [resp for resp in cached_responses if resp != last_used] if len(cached_responses) > 1 else cached_responses
                selected_response = random.choice(possible_responses)
                self.lru_cache.put('last_used_response', selected_response)

                sentences = re.split(r'(?<=[.!?])\s+', selected_response)
                for sentence in sentences:
                    self.core.speech_queue.put(sentence)
                threading.Thread(target=self.fetch_and_store, args=(query, query_hash, detected_intent)).start()
                return

        response = []
        for chunk in self.llm.get_response(query):
            if chunk.strip():
                self.core.speech_queue.put(chunk)
                response.append(chunk)

        response = ' '.join(response)
        intent_name = '.'.join(self.extract_key_phrases(query))

        threading.Thread(target=self.add_response, args=(query, query_hash, intent_name, response)).start()
        self.save_cache()
