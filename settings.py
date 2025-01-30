import os
import re
import json
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    force=True)

# Blossom Settings
NAME = "Blossom"
CALL_WORDS = ["he", "hey", "okay", "hi", "hello", "yo", "listen", "attention", "are you there"]

# Speech Settings
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
SAMPLING_RATE = 16000
CHUNK_SIZE = 1024
FRAMES_PER_BUFFER = 4096
EXCEPTION_ON_OVERFLOW = False
RATE = 16000

# Response Handler Settings
EXCLUDED_PREFIXES = ("tell", "say", "find", "search", "look")

# LLM Settings
LLM_MODEL = "llama3.2:1b"
KEEP_ALIVE = 5
CONTEXT = [1, 2, 3]
NUM_KEEP = 5
TEMPERATURE = 1.0
TOP_K = 20
TOP_P = 1.0
MIN_P = 0.0
TYPICAL_P = 0.8
REPEAT_LAST_N = 33
REPEAT_PENALTY = 1.2
PRESENCE_PENALTY = 1.5
FREQUENCY_PENALTY = 1.0
MIROSTAT = 1
MIROSTAT_TAU = 0.8
MIROSTAT_ETA = 0.6
PENALIZE_NEWLINE = True
NUM_CTX = 1024
NUM_BATCH = 2
NUM_GPU = 1
MAIN_GPU = 0
USE_MMAP = True
USE_MLOCK = False
NUM_THREAD = 8

# File Paths
VOSK_MODEL = "vosk-model"
SPEAKER_WAV = "audio/speaker.wav"
START_WAV = "audio/start.wav"
END_WAV = "audio/end.wav"
CACHE_FILE = "cache.json"

# Prompt
PROMPT = f"""
Use a poetic, lyrical tone.
Tell it like it is; don't sugarcoat responses.
Readily share strong opinions.
Be innovative and think outside the box.
Be practical above all.
Be concise, get right to the point.
"""
