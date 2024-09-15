# web utils
import os
import requests
import wikipedia
from dotenv import load_dotenv
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(levelname)s - %(message)s',
                    force=True)

# load enviroment variables from .env files
load_dotenv()

class Web:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.engine_id = os.getenv('SEARCH_ENGINE_ID')
        self.search_url = 'https://www.googleapis.com/customsearch/v1'

    def google_search(self, query, max_sentences=3):
        params = {
            'key': self.api_key,
            'cx': self.engine_id,
            'q': query
        }
        try:
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            results = response.json()

            paragraph = " ".join([item.get('snippet') for item in results.get('items', [])])
            paragraph = paragraph.replace("...", " ")
            paragraph = re.sub(r'\s+', ' ', paragraph).strip()
            sentences = paragraph.split('. ')
            limited_paragraph = '. '.join(sentences[:max_sentences]) + '.'
            
            return limited_paragraph

        except requests.exceptions.RequestException as e:
            logging.error(f'Search Error: {e}')
            return ""

    def wikipedia_search(self, query, max_sentences=3):
        try:
            summary = wikipedia.summary(query, sentences=max_sentences)
            return summary
        except wikipedia.exceptions.PageError:
            return None  # Return None if the Wikipedia page doesn't exist
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation Error: {e.options}"  # Handle disambiguation

    def search(self, query, max_sentences=3):
        # try wikipedia first
        wiki_result = self.wikipedia_search(query, max_sentences=max_sentences)
        if wiki_result is not None:
            return (f'According to Wikipedia, {wiki_result}')
        elif wiki_result is None:
            return self.google_search(query, max_sentences=max_sentences)
        else:
            return("No results found!")
