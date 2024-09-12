# Blossom
import os
import subprocess
from dflow import Dflow
import pyaudio
import json
import threading
from vosk import Model, KaldiRecognizer
import time
from TTS.api import TTS
#import logging

# Configure logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Core:
    def __init__(self, name):
        self.name = name
        self.agent = Dflow(self)
        self.model_path = 'vosk-model'
        self.model = self.load_vosk_model()
        self.recognizer = KaldiRecognizer(self.model, 16000) # 16 KHz sampling rate
        self.query = None # shared variable to store recognized speech
        self.speech_thread = None
        self.called = False # call flag
        self.call_words = ["hey", "okay", "hi", "yo", "listen", "attention", "are you there"] # define call words
        self.lock = threading.Lock()
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
        self.timeout = 5 # timeout duration
        self.last_active = time.time() # initialize with current time
        self.counter = 0
        self.shutdown_flag = threading.Event()

    def load_vosk_model(self):
        if not os.path.exists(self.model_path):
            print(f'Model not found at {self.model_path}, please check the path.')
            exit(1)
        return Model(self.model_path)

    def speak(self, text):
        try:
            self.tts.tts_to_file(text,
                    file_path="output.wav",
                    speaker_wav="speaker.wav",
                    language="en")
            result = subprocess.run(['aplay', 'output.wav'], capture_output=True)
            if result.returncode != 0:
                print(f'Error playing audio with aplay: {result.stderr}')
        except Exception as e:
            print(f'Error in TTS: {e}')
        print(f'{self.name}: {text}')

    def recognize_speech(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
        stream.start_stream()

        print("Listening...")

        try:
            while not self.shutdown_flag.is_set():
                data = stream.read(4096, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    if 'text' in result and result['text'].strip() != "":
                        with self.lock:
                            self.query = result['text'].strip() # update shared variable
                        print(f'Recognized: {self.query}')
        except IOError as e:
            print(f'IOError in audio stream: {e}')
        except Exception as e:
            print(f'Unexpected error in audio stream: {e}')
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("Audio stream terminated.")

    # hotword detection
    def get_call(self):
        while not self.shutdown_flag.is_set():
            with self.lock: # ensure thread safety
                if self.query and all([self.name.lower() in self.query.lower(), 
                                   any(word in self.query.lower() for word in self.call_words)]):
                    self.called = True
                    print("call detected!")
                    self.query = None
            time.sleep(0.1)

    def start_threads(self):
        # start speech recognition in a seperate thread
        self.speech_thread = threading.Thread(target=self.recognize_speech)
        self.speech_thread.daemon = True # ensures thread stops when main program exits
        self.speech_thread.start()

        self.call_thread = threading.Thread(target=self.get_call)
        self.call_thread.daemon = True # ensures thread stops when main program exits
        self.call_thread.start()

    def run(self):
        self.start_threads()

        try:
            while True:
                if self.called:
                    with self.lock: # for thread safety
                        if self.query:
                            print("processing...")
                            self.speak(self.agent.get_response(self.query))
                            self.called = False
                        self.query = None
                time.sleep(0.1) # reduce CPU usage

        except KeyboardInterrupt:
            print("Shutting down...")
            self.shutdown_flag.set() # signal threads to exit

            # wait for threads to finish
            if self.speech_thread:
                self.speech_thread.join()
            if self.call_thread:
                self.call_thread.join()
            print("All threads terminated.")

if __name__ == '__main__':
    core = Core('Blossom')
    core.run()
