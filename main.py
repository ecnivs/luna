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
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(levelname)s - %(message)s',
                    force=True)

class Core:
    def __init__(self, name):
        self.name = name
        self.agent = Dflow(self)
        self.model_path = 'vosk-model'
        self.model = self.load_vosk_model()
        self.recognizer = KaldiRecognizer(self.model, 16000) # 16 KHz sampling rate
        self.query = None # shared variable to store recognized speech
        self.called = False # call flag
        self.call_words = ["hey", "okay", "hi", "yo", "listen", "attention", "are you there"] # define call words
        self.lock = threading.Lock()
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
        self.shutdown_flag = threading.Event()

    def load_vosk_model(self):
        if not os.path.exists(self.model_path):
            logging.info(f'Model not found at {self.model_path}, please check the path.')
            exit(1)
        try:
            return Model(self.model_path)
        except ValueError as e:
            logging.error(f'Error loading Vosk model: {e}')

    def speak(self, text):
        try:
            self.tts.tts_to_file(text,
                    file_path="audio/output.wav",
                    speaker_wav="audio/speaker.wav",
                    language="en")
            self.play_audio("output.wav")
        except Exception as e:
            logging.error(f'Error in TTS: {e}')
        logging.info(f'{self.name}: {text}')

    def play_audio(self, text):
        result = subprocess.run(['ffplay', '-nodisp', '-autoexit', f'audio/{text}'], capture_output=True)
        if result.returncode != 0:
            logging.error(f'Error playing audio with ffplay: {result.stderr}')

    def recognize_speech(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
        stream.start_stream()

        logging.info("Listening...")

        try:
            while not self.shutdown_flag.is_set():
                data = stream.read(4096, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    if 'text' in result and result['text'].strip() != "":
                        with self.lock:
                            self.query = result['text'].strip() # update shared variable
                        logging.info(f'Recognized: {self.query}')
                time.sleep(0.1) # reduce CPU usage
        except IOError as e:
            logging.error(f'IOError in audio stream: {e}')
        except Exception as e:
            logging.error(f'Unexpected error in audio stream: {e}')
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            logging.info("Audio stream terminated.")

    # hotword detection
    def get_call(self):
        while not self.shutdown_flag.is_set():
            with self.lock: # ensure thread safety
                if self.query and all([self.name.lower() in self.query.lower(), 
                                   any(word in self.query.lower() for word in self.call_words)]):
                    self.called = True
                    self.play_audio("start.wav")
                    logging.info("call detected!")
                    _, query = self.query.lower().split(self.name.lower(), 1)
                    if query == "" or len(query.split(" ")) < 2:
                        self.query = None
            time.sleep(0.1) # reduce CPU usage

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
        logging.info("Threads started")

        try:
            while True:
                if self.called:
                    with self.lock: # for thread safety
                        if self.query:
                            logging.info("processing...")
                            self.play_audio("end.wav")
                            self.called = False
                            self.speak(self.agent.get_response(self.query))
                        self.query = None
                time.sleep(0.1) # reduce CPU usage

        except KeyboardInterrupt:
            logging.info("Shutting down...")
            self.shutdown_flag.set() # signal threads to exit

            # wait for threads to finish
            if self.speech_thread:
                self.speech_thread.join()
            if self.call_thread:
                self.call_thread.join()
            logging.info("All threads terminated.")

if __name__ == '__main__':
    core = Core('Blossom')
    core.run()
