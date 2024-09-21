import os
import google.cloud.dialogflow as dialogflow
from google.api_core.exceptions import DeadlineExceeded, InvalidArgument
import uuid
import socket

class Agent:
    def __init__(self):
        self.connected = False
        self.initialize()

    def initialize(self):
        if self.check_internet:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'
            self.project_id = 'blossom-jwv9'
            self.language = 'en'
            self.session_id = str(uuid.uuid4())
            self.connected = None
            self.session_client = dialogflow.SessionsClient()
            self.session = self.session_client.session_path(self.project_id, self.session_id)
            self.connected = True

    def check_internet(self):
        try:
            # Try to connect to Google's DNS server
            socket.create_connection(("8.8.8.8", 53))
            return True
        except OSError:
            return False

    def get_response(self, query, timeout=5):
        if not self.connected:
            self.initialize()
        self.text_input = dialogflow.TextInput(text=query, language_code=self.language)
        self.query_input = dialogflow.QueryInput(text=self.text_input)
        try:
            self.response = self.session_client.detect_intent(session=self.session,
                                                              query_input=self.query_input,
                                                              timeout=timeout)
            self.update()
        except DeadlineExceeded:
            return "DeadlineExceeded"
        except InvalidArgument:
            return "InvalidArgument"
        except Exception as e:
            return f"Unexpected Error: {e}"

        return None
        
    def update(self):
        self.query_text = self.response.query_result.query_text
        self.detected_intent = self.response.query_result.intent.display_name
        self.detected_intent_confidence = self.response.query_result.intent_detection_confidence 
        self.fulfillment_text = self.response.query_result.fulfillment_text
        self.fulfillment_message = self.response.query_result.fulfillment_messages
