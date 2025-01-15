# Blossom
from res_handler import ResponseHandler
from settings import *
import pyaudio
from vosk import Model, KaldiRecognizer
import time
from TTS.api import TTS
import torch
import wave
import queue
import uuid
import glob

class Core:
    def __init__(self):
        self.name = NAME
        self.model = VOSK_MODEL
        self.query = None
        self.called = False
        self.is_playing = False

        self.on_init()

    def on_init(self):
        self.lock = threading.Lock()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tts = TTS(model_name=TTS_MODEL).to(self.device)
        self.shutdown_flag = threading.Event()
        self.audio = pyaudio.PyAudio()
        self.model = self.load_vosk_model()
        self.recognizer = KaldiRecognizer(self.model, SAMPLING_RATE)
        self.handler = ResponseHandler(self)
        self.speak_queue = queue.Queue()
        self.play_queue = queue.Queue()

    def load_vosk_model(self):
        if not os.path.exists(self.model):
            logging.info(f'Model not found at {self.model}, please check the path.')
            exit(1)
        try:
            return Model(self.model)
        except ValueError as e:
            logging.error(f'Error loading Vosk model: {e}')
            exit(1)

    def speak(self, text, queue = False):
        output_wav = f"{uuid.uuid4().hex}_temp.wav"
        try:
            self.tts.tts_to_file(text,
                    file_path = output_wav,
                    speaker_wav = SPEAKER_WAV,
                    language="en")
            if queue:
                self.play_queue.put(output_wav)
            else:
                self.play_audio(output_wav)
        except Exception as e:
            logging.error(f'Error in TTS: {e}')

    def play_audio(self, filename):
        def audio_thread():
            self.is_playing = True
            stream = None
            try:
                with wave.open(filename, 'rb') as wf:
                    chunk_size = min(CHUNK_SIZE, wf.getnframes())
                    stream = self.audio.open(
                        format=self.audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        frames_per_buffer=chunk_size)

                    data = wf.readframes(wf.getnframes())
                    stream.write(data)
                    time.sleep(0.1)
                    stream.stop_stream()

                if "_temp" in filename:
                    os.remove(filename)
                self.is_playing = False

            except Exception as e:
                logging.error(f'Error during playback of {filename}: {e}')
            finally:
                if stream is not None:
                    if stream.is_active():
                        stream.stop_stream()
                    stream.close()

        threading.Thread(target=audio_thread, daemon=True).start()

    def recognize_speech(self):
        stream = self.audio.open(format=pyaudio.paInt16,
                        channels = 1,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = FRAMES_PER_BUFFER)
        stream.start_stream()

        self.speak(self.handler.get_response((f"Hey {self.name}")))
        logging.info("Listening...")

        try:
            while not self.shutdown_flag.is_set():
                data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=EXCEPTION_ON_OVERFLOW)
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    if 'text' in result and result['text'].strip() != "":
                        with self.lock:
                            self.query = result['text'].strip()
                        logging.info(f'Recognized: {self.query}')

                with self.lock:
                    if not self.query:
                        continue

                    # lowercase and split
                    query_lower = self.query.lower().strip()
                    query_words = query_lower.split()
                    name_lower = self.name.lower()

                    # hotword detection
                    if any(word in query_lower for word in CALL_WORDS):
                        for word in CALL_WORDS:
                            if f'{word} {name_lower}' in query_lower:
                                self.called = True
                                logging.info("call detected!")
                                _, query = query_lower.split(f'{word} {name_lower}', 1)
                                if query.strip() == "" or len(query.strip().split()) < 2:
                                    self.query = None
                                    self.play_audio(START_WAV)
                                else:
                                    self.query = query.strip()
                                break

                    if self.called is not True:
                        if query_words[0] == name_lower and len(query_words) > 2:
                            self.called = True
                            logging.info("call detected!")
                            self.query = " ".join(query_words[1:])

                        elif query_words[-1] == name_lower and len(query_words) > 2:
                            self.called = True
                            logging.info("call detected!")
                            self.query = " ".join(query_words[:-1])

                time.sleep(0.1)
        except IOError as e:
            logging.error(f'IOError in audio stream: {e}')
        except Exception as e:
            logging.error(f'Unexpected error in audio stream: {e}')
        finally:
            stream.stop_stream()
            stream.close()
            self.audio.terminate()
            logging.info("Audio stream terminated.")

    def process_queue(self):
        if not self.speak_queue.empty():
            self.speak(self.speak_queue.get(), queue = True)
        if not self.play_queue.empty():
            if not self.is_playing:
                self.play_audio(self.play_queue.get())

    def run(self):
        self.speech_thread = threading.Thread(target=self.recognize_speech, daemon=True)
        self.speech_thread.start()

        try:
            while True:
                self.process_queue()
                if self.called:
                    with self.lock:
                        if self.query:
                            logging.info("processing...")
                            self.play_audio(END_WAV)
                            self.called = False
                            self.handler.handle(self.query)
                        self.query = None
                time.sleep(0.1)

        except KeyboardInterrupt:
            logging.info("Shutting down...")
            self.shutdown_flag.set()
            self.handler.save_cache()
            self.handler.handler.unload_model()

            files = glob.glob("*_temp.wav")
            for file in files:
                os.remove(file)

            if self.speech_thread:
                self.speech_thread.join()
            logging.info("All threads terminated.")

if __name__ == '__main__':
    core = Core()
    core.run()
