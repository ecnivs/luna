# Response Handler
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from llm_handler import LlmHandler
from settings import *
from cache_handler import LRUCache, LFUCache
from action_handler import ActionHandler
import hashlib
import random

class ResponseHandler:
    """
    Handles response caching and retrieval for the chatbot.
    Uses LRU (Least Recently Used) and LFU (Least Frequently Used) caching strategies
    to optimize response storage and reuse.
    """
    def __init__(self, core):
        self.core = core
        self.lru_cache = LRUCache(MAX_LRU_SIZE)
        self.lfu_cache = LFUCache(MAX_LFU_SIZE)

        self.on_init()

    def on_init(self):
        """Initializes the necessary components for the class instance."""
        self.llm = LlmHandler(self.core)
        self.cache = self.load_cache()
        self.stemmer = PorterStemmer()
        self.action = ActionHandler(self.core)

    @staticmethod
    def hash_query(query):
        """Hashes a  query using MD5 for consistent cache keys."""
        return hashlib.md5(query.encode()).hexdigest()

    def load_cache(self):
        """Loads cached responses from file, initializing LRU and LFU caches."""
        if not os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'w') as file:
                json.dump({'lru': {}, 'lfu': {}}, file)
            return

        with open(CACHE_FILE, 'r') as file:
            data = json.load(file)
            self.lru_cache.load(data.get('lru', {}))
            self.lfu_cache.load(data.get('lfu', {}))

    def save_cache(self):
        """Saves the current cache state to a file."""
        with open(CACHE_FILE, 'w') as file:
            json.dump({'lru': self.lru_cache.to_dict(), 'lfu': self.lfu_cache.to_dict()}, file)

    def extract_key_phrases(self, query):
        """Extracts key phrases from the query using stemming and removes stop words."""
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
        """Fetches a fresh response from the LLM and stores it in the cache."""
        new_response = []
        for chunk in self.llm.get_response(query):
            if chunk.strip():
                new_response.append(chunk)

        new_response = ' '.join(new_response)
        self.add_response(query_hash, intent, new_response)

    def add_response(self, query_hash, intent, response):
        """Adds a response to the LFU cache under the given intent and updates the LRU cache."""
        response = response.replace(USERNAME, "{NAME}")
        existing_responses = self.lfu_cache.get(intent) or []

        if response not in existing_responses:
            existing_responses.append(response)
            self.lfu_cache.put(intent, existing_responses)

        self.lru_cache.put(query_hash, {'intent': intent})
        self.save_cache()

    def do(self, data):
        action_name = data.get('action')
        parameters = data.get('parameters')
        if hasattr(self.action, action_name):
            return getattr(self.action, action_name)(**parameters)

    def handle(self, query):
        """
        Processes a user query:
        - Checks the cache for responses if at least 3 exist for the intent.
        - Uses the last response tracking to avoid immediate repetition.
        - Fetches a new response in the background while serving a cached response.
        """
        query_hash = self.hash_query(query.lower())
        cached_data = self.lru_cache.get(query_hash) or self.lfu_cache.get(query_hash)

        if cached_data:
            detected_intent = cached_data['intent']
            cached_responses = self.lfu_cache.get(detected_intent) or []

            if len(cached_responses) >= 2:
                last_used = self.lru_cache.get('last_used_response')
                possible_responses = [res for res in cached_responses if res != last_used] if len(cached_responses) > 1 else cached_responses
                selected_response = random.choice(possible_responses)
                self.lru_cache.put('last_used_response', selected_response)

                sentences = re.split(r'(?<=[.!?])\s+', selected_response)
                for sentence in sentences:
                    sentence = sentence.replace("{NAME}", USERNAME)
                    self.core.speech_queue.put(sentence)
                if not self.llm.cam:
                    threading.Thread(target=self.fetch_and_store, args=(query, query_hash, detected_intent)).start()
                return

        response = []
        for chunk in self.llm.get_response(query):
            if chunk.strip():
                self.core.speech_queue.put(chunk)
                response.append(chunk)

        response = ' '.join(response)
        intent_name = '.'.join(self.extract_key_phrases(query))

        if not self.llm.cam:
            threading.Thread(target=self.add_response, args=(query_hash, intent_name, response)).start()
