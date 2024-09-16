# Web Handler
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

# Load environment variables from .env file
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

            for item in results.get('items', []):
                snippet = item.get('snippet')
                if snippet:
                    clean_snippet = self.clean_text(snippet)
                    
                    if self.is_fragmented(clean_snippet):
                        continue
                    
                    sentences = clean_snippet.split('. ')
                    limited_paragraph = '. '.join(sentences[:max_sentences]) + '.'

                    if len(limited_paragraph) > 250:
                        return sentences[0] + '.'

                    return limited_paragraph

            return "No relevant information found."

        except requests.exceptions.RequestException as e:
            logging.error(f'Search Error: {e}')
            return ""

    def clean_text(self, text):
        # Remove common unwanted phrases, dates, and formatting
        text = re.sub(r'(?i)(learn how|according to|click here|watch)', '', text)
        text = re.sub(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b \d{1,2}, \d{4}', '', text)
        text = text.replace('...', ' ')  # Replace ellipses with a space
        return re.sub(r'\s+', ' ', text).strip()  # Remove multiple spaces

    def is_fragmented(self, text):
        # Check if the text starts mid-sentence or is incomplete
        return text[0].islower()  # Assuming a snippet starting with a lowercase letter is likely fragmented

    def wikipedia_search(self, query, max_sentences=2):
        try:
            summary = wikipedia.summary(query, sentences=max_sentences)
            if len(summary) > 250:
                sentences = summary.split('. ')
                return sentences[0] + '.'
            return summary
        except wikipedia.exceptions.PageError:
            return None
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Disambiguation Error: {e.options}"

    def search(self, query):
        # Try Wikipedia first
        wiki_result = self.wikipedia_search(query)
        if wiki_result:
            return f"According to Wikipedia, {wiki_result}"
        
        # Fall back to Google search if Wikipedia doesn't work
        google_result = self.google_search(query)
        if google_result:
            return google_result
        
        return "No results found!"
