# LLM Handler
import requests
from settings import *

class LlmHandler:
    def __init__(self):
        self.model = LLM_MODEL
        self.session = requests.Session()
        self.get_prompt()

    def get_prompt(self):
        try:
            with open(PROMPT_FILE, 'r') as file:
                self.prompt = file.read()
        except FileNotFoundError:
            default = f"You are an AI Assistant named {NAME}"
            with open(PROMPT_FILE, 'w') as file:
                file.write(default)
            self.prompt = default
            logging.error(f"'{PROMPT_FILE}' not found. Created new one.")

    def unload_model(self):
        data = {
            "model": self.model,
            "keep_alive": 0
        }
        self.session.post("http://localhost:11434/api/generate", json=data)

    def get_response(self, query):
        data = {
            "model": self.model,
            "stream": True,
            "context": CONTEXT,
            "prompt": f"{query}",
            "system": f"{self.prompt}",
            "options": {
                "num_keep": NUM_KEEP,
                "temperature": TEMPERATURE,
                "top_k": TOP_K,
                "top_p": TOP_P,
                "min_p": MIN_P,
                "typical_p": TYPICAL_P,
                "repeat_last_n": REPEAT_LAST_N,
                "repeat_penalty": REPEAT_PENALTY,
                "presence_penalty": PRESENCE_PENALTY,
                "frequency_penalty": FREQUENCY_PENALTY,
                "mirostat": MIROSTAT,
                "mirostat_tau": MIROSTAT_TAU,
                "mirostat_eta": MIROSTAT_ETA,
                "penalize_newline": PENALIZE_NEWLINE,
                "num_ctx": NUM_CTX,
                "num_batch": NUM_BATCH,
                "num_gpu": NUM_GPU,
                "main_gpu": MAIN_GPU,
                "use_mmap": USE_MMAP,
                "use_mlock": USE_MLOCK,
                "num_thread": NUM_THREAD
            }
        }
        response = self.session.post(
            "http://localhost:11434/api/generate",
            json=data,
            stream=True
        )
        for chunk in response.iter_content(chunk_size=512):
            chunk_str = chunk.decode("utf-8")
            try:
                chunk_json = json.loads(chunk_str)
                yield chunk_json.get("response", "")
            except json.JSONDecodeError:
                continue
