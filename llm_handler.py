import requests

class LlmHandler:
    def __init__(self, core):
        self.name = core.name

    def get_response(self, query):
        data = {
            "model": "llama2-uncensored",
            "prompt": f"{query}",
            "stream": False,
            "system": f"Your name is {self.name}"
        }
        response = requests.post("http://localhost:11434/api/generate", json=data)
        return (response.json()["response"])
