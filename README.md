# Blossom (In Development)

## Overview
This repository is dedicated to the software development of **Blossom**, a humanoid robot. The project aims to integrate real-time control, object detection, and voice interaction capabilities.

## Tech Stack
* Programming Language: `Python`
* Speech Recognition: `Vosk`
* Text to Speech Synthesis: `Coqui TTS`
* Natural Language Processing: `Google Dialogflow`
* Audio Processing: `PyAudio`
* Concurrency: `Threading`
* Data Handling: `JSON`

## Prerequisites
* Python 3.x (Tested with Python 3.11 using pyenv)
* Required Python libraries (listed in `requirements.txt`)
* [Vosk model](https://alphacephei.com/vosk/models)
* Dialogflow Key
* Access to Google Cloud for Dialogflow setup
* Google Search Engine ID
* Google Search API Key

## Installation
1. Clone the repository:
```bash
git clone https://github.com/ecnivs/Blossom.git
```
2. Navigate to the project directory:
```bash
cd Blossom
```
3. Set up Python with pyenv:
```bash
pyenv install 3.11
pyenv local 3.11
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Run the Software:
```bash
python main.py
```

## Configuration
1. *Vosk Model*: Download and place Vosk model in the directory.
2. *Dialogflow*: Obtain and place Dialogflow key.json in the directory
3. *Google Custom Search*: Obtain your Google Search Engine ID and API Key and create .env file:
```bash
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
GOOGLE_SEARCH_API_KEY=your_search_api_key
```

### I'd appreciate any feedback or code reviews you might have!
