"""
Blossom Configuration File

This file contains all configurable settings for Blossom, including
logging, speech processing, response handling, and LLM configurations.

Modify these values based on system requirements and desired behavior.
"""
import os
import re
import json
import threading
import logging
from dotenv import load_dotenv

# Load .env
load_dotenv()

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(level=logging.DEBUG, # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(levelname)s - %(message)s', # Define log message format
                    force=True) # Override existing logging settings

# -------------------------------
# File Paths
# -------------------------------
VOSK_MODEL = "vosk-model"  # Path to the Vosk speech recognition model
SPEAKER_WAV = "audio/speaker.wav"  # Path to the speaker voice sample
START_WAV = "audio/start.wav"  # Path to start sound
END_WAV = "audio/end.wav"  # Path to end sound
CACHE_FILE = "json/cache.json"  # Path to the cache file for stored data
ACTIONS_FILE = "json/actions.json"
USER_FILE = "json/user.json"

# -------------------------------
# Assistant Settings
# -------------------------------
NAME = "Blossom" # Name of the assistant
CALL_WORDS = [
    "he", "hey", "okay", "hi", "hello", "yo", "listen", "attention", "are you there"
] # Words that trigger the assistant
with open(USER_FILE, 'r') as file:
    USER_DATA = json.load(file)
USERNAME = USER_DATA['name']

# -------------------------------
# Speech Processing Settings
# -------------------------------
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2" # Text-to-speech model
SAMPLING_RATE = 16000 # Audio sampling rate (Hz)
CHUNK_SIZE = 1024 # Size of each audio chunk
FRAMES_PER_BUFFER = 4096 # Buffer size for audio processing
EXCEPTION_ON_OVERFLOW = False # Prevent exceptions on buffer overflow
RATE = SAMPLING_RATE # Audio rate (should match SAMPLING_RATE)

# -------------------------------
# Response Handler Settings
# -------------------------------
EXCLUDED_PREFIXES = ("tell", "say", "find", "search", "look") # Words to ignore at first index
MAX_LRU_SIZE = 1000 # Max size for Least Recently Used (LRU) cache
MAX_LFU_SIZE = 5000 # Max size for Least Frequently Used (LFU) cache
with open(ACTIONS_FILE, 'r') as file:
    ACTIONS = json.load(file)

# -------------------------------
# LLM Configuration
# -------------------------------
ENDPOINT = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
MAX_CONTEXT_SIZE = 5

# -------------------------------
# Assistant Prompt Configuration
# -------------------------------
PROMPT = f"""
Respond directly and clearly—no fluff, no detours.
Tell it like it is; don't sugarcoat responses.
Share strong opinions and expressions freely.
Be innovative, think outside the box, and stay practical.
Stay concise—get to the point fast.
Creativity serves truth, not distraction.

Assume my name is {USERNAME}. Address me as such when relevant.
Here are my details: {USER_DATA}

When given an image, process it as direct input—what you see is what exists.
Do not treat it like a "picture" but as immediate reality.
Only describe details if explicitly asked.
Assume the person in the image is me ({USERNAME}) unless context suggests otherwise.

You have access to tools.
If and only when asked to perform an action, output a JSON object with 'action', 'parameters' and 'response'(not null) instead of answering directly.
Your available actions are {ACTIONS}
"""
