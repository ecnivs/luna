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
import sounddevice as sd
import subprocess

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

    def load_vosk_model(self):
        if not os.path.exists(self.model_path):
            print(f'Model not found at {self.model_path}, please check the path.')
            exit(1)
        return Model(self.model_path)

    def speak(self, text):
        #subprocess.run(['espeak', '-ven+f5', '-s 150', '-p 80', text])
        self.tts.tts_to_file(text,
                file_path="output.wav",
                speaker_wav="speaker.wav",
                language="en")
        subprocess.run(['aplay', 'output.wav'])
        print(text)

    def recognize_speech(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
        stream.start_stream()

        print("Listening...")

        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                if 'text' in result and result['text'].strip() != "":
                    with self.lock:
                        self.query = result['text'].strip() # update shared variable
                    print(f'Recognized: {self.query}')

    def get_call(self):
        while True:
            with self.lock: # for thread safety
                if self.query and all([self.name.lower() in self.query.lower(), 
                                   any(word in self.query.lower() for word in self.call_words)]):
                    self.called = True
                    print("call detected!")
                    self.query = None

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

        while True:
            if self.called:
                with self.lock: # for thread safety
                    if self.query:
                        print("processing...")
                        self.speak(self.agent.get_response(self.query))

                        # for testing purpose
                        print(f'{self.agent.response.query_result.intent_detection_confidence} '
                            f'{self.agent.response.query_result.intent.display_name}')
                        
                        self.called = False # reset call flag
                    self.query = None
            
            time.sleep(0.1) # slight sleep to avoid CPU overload

if __name__ == '__main__':
    core = Core('Blossom')
    core.run()
