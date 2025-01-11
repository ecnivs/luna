import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    force=True)

class LlmHandler:
    def __init__(self, core):
        self.name = core.name
        self.context = []
        self.get_prompt()

    def get_prompt(self):
        try:
            with open('.prompt.txt', 'r') as file:
                self.prompt = file.read()
        except FileNotFoundError:
            default = f"You are a female AI Assistant named {self.name}"
            with open('.prompt.txt', 'w') as file:
                file.write(default)
            logging.error("'.prompt.txt' not found. Creating new one.")

    def add_to_context(self, role, content):
        self.context.append({"role": role, "content": content})

    def get_response(self, query):
        data = {
            "model": "llama2-uncensored",
            "prompt": f"{query}",
            "stream": False,
            "system": f"{self.prompt}"
        }
        response = requests.post("http://localhost:11434/api/generate", json=data)
        return (response.json()["response"])
