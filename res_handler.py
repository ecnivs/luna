# response handler
from llm_handler import LlmHandler

class ResponseHandler:
    def __init__(self, core):
        self.handler = LlmHandler(core)

    def handle(self, query):
        response = self.handler.get_response(query)
        return response
