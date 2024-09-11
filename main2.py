import sounddevice as sd
from TTS.api import TTS

# Load the model with GPU support
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

# Specify the language code for English
language_code = "en"

# Example of a commonly available speaker ID for English; this might need adjustment
speaker_id = "en_1"  # This is a placeholder; replace with an actual ID if needed

# Generate speech with the specified language and speaker
text = "Hello, this is an example sentence using the xtts_v2 model in English."
wav = tts.tts(text, language=language_code, speaker=speaker_id)

# Play the generated audio directly
faster_rate = tts.synthesizer.output_sample_rate * 1.15  # Increase speed by 15%
sd.play(wav, samplerate=int(faster_rate))  # Play at faster speed
sd.wait()  # Wait until the sound finishes playing

