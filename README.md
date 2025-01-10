# Blossom

## Overview
This repository is dedicated to the software development of **Blossom**, a virtual assistant. The project aims to deliver a seamless and responsive user experience.

## Prerequisites
* Python 3.x (Tested with Python 3.11 using pyenv)
* Required Python libraries (listed in `requirements.txt`)
* [Vosk model](https://alphacephei.com/vosk/models)
* [Ollama](https://ollama.com/)
* [Large Language Model (LLM)](https://en.wikipedia.org/wiki/Large_language_model)
* Dialogflow Key
* Access to Google Cloud for Dialogflow setup

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
5. Download an LLM:
```bash
ollama pull llama2-uncensored
```
6. Run the Software:
```bash
python main.py
```

## Configuration
1. **Vosk Model**: Download and place `Vosk-model` in the directory.
2. **Dialogflow**: Obtain and place Dialogflow `key.json` in the directory

## Contributing
We appreciate any feedback or code reviews! Feel free to:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a pull request

### I'd appreciate any feedback or code reviews you might have!
