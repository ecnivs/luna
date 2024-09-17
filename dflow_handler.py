import os
import google.cloud.dialogflow as dialogflow
from google.api_core.exceptions import InvalidArgument

class Agent:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'
        self.project_id = 'blossom-jwv9'
        self.language = 'en'
        self.session_id = 'blossom'
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

    def get_response(self, query):
        self.text_input = dialogflow.TextInput(text=query, language_code=self.language)
        self.query_input = dialogflow.QueryInput(text=self.text_input)
        try:
            self.response = self.session_client.detect_intent(session=self.session, query_input=self.query_input)
            self.update()
        except InvalidArgument:
            raise
        
    def update(self):
        self.query_text = self.response.query_result.query_text
        self.detected_intent = self.response.query_result.intent.display_name
        self.detected_intent_confidence = self.response.query_result.intent_detection_confidence 
        self.fulfillment_text = self.response.query_result.fulfillment_text
        self.fulfillment_message = self.response.query_result.fulfillment_messages
