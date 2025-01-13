import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    force=True)

class LlmHandler:
    def __init__(self, core):
        self.name = core.name
        self.model = "llama2-uncensored"
        self.session = requests.Session()
        self.get_prompt()

    def get_prompt(self):
        try:
            with open('.prompt.txt', 'r') as file:
                self.prompt = file.read()
        except FileNotFoundError:
            default = f"You are an AI Assistant named {self.name}"
            with open('.prompt.txt', 'w') as file:
                file.write(default)
            logging.error("'.prompt.txt' not found. Creating new one.")

    def unload_model(self):
        data = {
            "model": self.model,
            "keep_alive": 0
        }
        self.session.post("http://localhost:11434/api/generate", json=data)

    def get_response(self, query):
        data = {
            "model": self.model,
            "stream": False,
            "context": [1, 2, 3],
            "system": f"{self.prompt}",
            "prompt": f"{query}",
            "options": {
                "num_keep": 5,
                "num_predict": 100,
                "temperature": 0.8,
                "top_k": 20,
                "top_p": 0.9,
                "min_p": 0.0,
                "typical_p": 0.7,
                "repeat_last_n": 33,
                "repeat_penalty": 1.2,
                "presence_penalty": 1.5,
                "frequency_penalty": 1.0,
                "mirostat": 1,
                "mirostat_tau": 0.8,
                "mirostat_eta": 0.6,
                "penalize_newline": True,
                "num_ctx": 1024,
                "num_batch": 2,
                "num_gpu": 1,
                "main_gpu": 0,
                "vocab_only": False,
                "use_mmap": True,
                "use_mlock": False,
                "num_thread": 8
            }
        }
        response = self.session.post("http://localhost:11434/api/generate", json=data)
        return (response.json()["response"])
