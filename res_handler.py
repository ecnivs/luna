# response handler
from web_handler import WebHandler
from dflow_handler import Agent
import spacy

class ResponseHandler:
    def __init__(self, core):
        self.web = WebHandler()
        self.agent = Agent()
        self.core = core
        self.nlp = spacy.load("en_core_web_sm")

    def extract_key_phrases(self, query):
        doc = self.nlp(query)
        phrases = [chunk.text for chunk in doc.noun_chunks if any(token.pos_ in ['PROPN', 'NOUN'] for token in chunk)]
        return phrases

    def handle(self, query):
        self.agent.get_response(query)
        if 'web.search' in self.agent.detected_intent:
            return self.web.search(self.extract_key_phrases(query))
        else:
            return self.agent.fulfillment_text
