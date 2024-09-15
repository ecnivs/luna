# response handler
from web_utils import Web
from dflow_handler import Agent

class ResponseHandler:
    def __init__(self, core):
        self.web = Web()
        self.agent = Agent()
        self.core = core

    def handle(self, query):
        self.agent.get_response(query)
        if 'web.search' in self.agent.detected_intent:
            try:
                _, query = query.lower().split(self.core.name.lower(), 1)
            finally:
                return self.web.search(query)
        else:
            return self.agent.fulfillment_text
