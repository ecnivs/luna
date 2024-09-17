# Web handler
import os
import re
import requests
import wikipedia
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
from transformers import BartTokenizer, BartForConditionalGeneration
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(levelname)s - %(message)s',
                    force=True)

# Load environment variables from .env file
load_dotenv()

class WebHandler:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.engine_id = os.getenv('SEARCH_ENGINE_ID')
        self.search_url = 'https://www.googleapis.com/customsearch/v1'
        
        # Initialize BART model and tokenizer
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    def google_search(self, query, num_results=3):
        logging.debug(f'Performing Google search for query: {query}')
        params = {
            'key': self.api_key,
            'cx': self.engine_id,
            'q': query,
            'num': num_results
        }
        try:
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            results = response.json()
            urls = [item['link'] for item in results.get('items', [])]
            logging.debug(f'Google search results: {urls}')
            return urls

        except requests.exceptions.RequestException as e:
            logging.error(f'Search Error: {e}')
            return []

    def extract_content_from_url(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            return content
        except Exception as e:
            logging.error(f'Error extracting content from {url}: {e}')
            return ""

    def summarize_with_bart(self, text):
        inputs = self.tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
        summary_ids = self.model.generate(
            inputs['input_ids'], 
            max_length=150, 
            min_length=40, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
        if len(summary) > 250:
            summary = summary[:250]
            summary = re.sub(r'([.!?])[^.!?]*$', r'\1', summary)
        return summary

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
        except Exception as e:
            return f"Search Error: {e}"

    def fetch_and_summarize_url(self, url):
        content = self.extract_content_from_url(url)
        if content:
            return self.summarize_with_bart(content)
        return ""
    
    def search(self, query):
        wiki_result = self.wikipedia_search(query)
        if wiki_result:
            return f"According to Wikipedia, {wiki_result}"
    
        google_urls = self.google_search(query)
        if not google_urls:
            return "No results found!"

        summaries = []
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust concurrency as needed
            future_to_url = {executor.submit(self.fetch_and_summarize_url, url): url for url in google_urls}
            for future in as_completed(future_to_url):
                summary = future.result()
                if summary:
                    summaries.append(summary)
    
        if summaries:
            return summaries[0]
    
        return "No relevant information found from Google search."
