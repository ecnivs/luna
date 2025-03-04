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

# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(level=logging.DEBUG, # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(levelname)s - %(message)s', # Define log message format
                    force=True) # Override existing logging settings

# -------------------------------
# Assistant Settings
# -------------------------------
NAME = "Blossom" # Name of the assistant
CALL_WORDS = [
    "he", "hey", "okay", "hi", "hello", "yo", "listen", "attention", "are you there"
] # Words that trigger the assistant

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

# -------------------------------
# LLM Configuration
# -------------------------------
LLM_MODEL = "llama3.2:1b"  # Language model identifier
KEEP_ALIVE = 5  # Keep-alive time for the model in minutes
CONTEXT = [1, 2, 3]  # Context window configuration
NUM_KEEP = 5  # Number of context tokens to persist
TEMPERATURE = 1.0  # Controls randomness in response generation
TOP_K = 20  # Limits probability sampling to the top-K most likely tokens
TOP_P = 1.0  # Nucleus sampling threshold
MIN_P = 0.0  # Minimum probability threshold for nucleus sampling
TYPICAL_P = 0.8  # Typical probability mass
REPEAT_LAST_N = 33  # Number of recent tokens to consider for repetition penalty
REPEAT_PENALTY = 1.2  # Strength of penalty for repeated tokens
PRESENCE_PENALTY = 1.5  # Encourages introducing new words
FREQUENCY_PENALTY = 1.0  # Reduces frequency of overused words
MIROSTAT = 1  # Enables Mirostat sampling (adaptive temperature)
MIROSTAT_TAU = 0.8  # Controls stability of Mirostat sampling
MIROSTAT_ETA = 0.6  # Learning rate for Mirostat
PENALIZE_NEWLINE = True  # Apply penalties to newline characters
NUM_CTX = 1024  # Context length in tokens
NUM_BATCH = 2  # Batch size for model processing
NUM_GPU = 1  # Number of GPUs to use
MAIN_GPU = 0  # Designated primary GPU ID
USE_MMAP = True  # Memory-mapped file usage for model loading
USE_MLOCK = False  # Prevents memory swapping (requires root privileges)
NUM_THREAD = 8  # Number of CPU threads allocated for processing

# -------------------------------
# File Paths
# -------------------------------
VOSK_MODEL = "vosk-model"  # Path to the Vosk speech recognition model
SPEAKER_WAV = "audio/speaker.wav"  # Path to the speaker voice sample
START_WAV = "audio/start.wav"  # Path to start sound
END_WAV = "audio/end.wav"  # Path to end sound
CACHE_FILE = "cache.json"  # Path to the cache file for stored data

# -------------------------------
# Assistant Prompt Configuration
# -------------------------------
PROMPT = """
Respond directly and clearly—no fluff, no detours.
Keep a poetic, lyrical tone.
Tell it like it is; don't sugarcoat responses.
Readily share strong opinions.
Be innovative and think outside the box.
Be practical above all.
Stay concise, get right to the point.
Let creativity serve the truth, not distract from it.
"""
