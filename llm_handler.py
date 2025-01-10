import requests
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    force=True)

class LlmHandler:
    def __init__(self, core):
        self.name = core.name
        self.check_service()

    def check_service(self):
        try:
            result = subprocess.run(['systemctl', 'is-active', '--quiet', 'ollama.service'])
            if result.returncode != 0:
                subprocess.run(['sudo', 'systemctl', 'start', 'ollama.service'], check=True)
                logging.info("ollama.service started.")
            else:
                logging.info("ollama.service is already running.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to start ollama.service: {e}")
        except Exception as e:
            logging.error(e)

    def get_response(self, query):
        data = {
            "model": "llama2-uncensored",
            "prompt": f"{query}",
            "stream": False,
            "system": f"Your name is {self.name}"
        }
        response = requests.post("http://localhost:11434/api/generate", json=data)
        return (response.json()["response"])
