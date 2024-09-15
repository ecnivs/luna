# response handler
from web_utils import Web
from dflow import Dflow

class ResponseHandler:
    def __init__(self):
        self.web = Web()
        self.agent = Dflow()

    def handle(self, query):
        return self.agent.get_response(query)
