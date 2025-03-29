# LLM Handler
from settings import *
import base64
import cv2
import requests
import json

class LlmHandler:
    def __init__(self, core):
        self.core = core
        self.prompt = f"You are an AI Assistant named {NAME}.\n{PROMPT}"
        self.session = requests.Session()
        self.context = []
        self.cam = False

    def is_json(self, string):
        try:
            json.loads(string)
            return True
        except json.JSONDecodeError:
            return False

    def get_image(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            logging.error("Camera could not be accessed.")
            return None

        ret, frame = cap.read()
        cap.release()

        if not ret:
            logging.error("Could not read frame.")

        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode('utf-8')

    def get_payload(self, query, cam = False):
        self.context.append(f"User: {query}")

        if len(self.context) > MAX_CONTEXT_SIZE:
            self.context.pop(0)

        context_text = "\n".join(self.context)

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": self.prompt},
                        {"text": context_text}
                    ]
                }
            ]
        }

        if not self.cam and not cam:
            image_data = None
        else:
            image_data = self.get_image()

        if image_data:
            payload["contents"][0]["parts"].append(
                {"inline_data": {"mime_type": "image/jpeg", "data": image_data}}
            )

        return payload


    def get_response(self, query, cam = False):
        response = self.session.post(ENDPOINT, json=self.get_payload(query, cam = cam))

        if response.status_code == 200:
            response_text = str(response.json()["candidates"][0]["content"]["parts"][0]["text"])
        else:
            response_text = str("Error:", response.text)

        self.context.append(f"{NAME}: {response_text}")
        if len(self.context) > MAX_CONTEXT_SIZE:
            self.context.pop(0)
        return response_text
