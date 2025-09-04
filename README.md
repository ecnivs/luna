<h1 align="center">Luna</h1>
<p align="center"><em>SEAMLESS.INTELLIGENT.SECURE - Your Virtual Assistant</em></p>

![swappy-20250213-101131](https://github.com/user-attachments/assets/d5bffa73-92b5-48e2-8e53-69e0f54f6dcd)

<p align="center">
  <a href="https://github.com/ecnivs/luna/stargazers">
    <img src="https://img.shields.io/github/stars/ecnivs/luna?style=flat-square">
  </a>
  <a href="https://github.com/ecnivs/luna/issues">
    <img src="https://img.shields.io/github/issues/ecnivs/luna?style=flat-square">
  </a>
  <a href="https://github.com/ecnivs/luna/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ecnivs/luna?style=flat-square">
  </a>
  <img src="https://img.shields.io/badge/python-3.13%2B-blue?style=flat-square">
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-informational?style=flat-square">
</p>

## 🏆 Recognition
> Secured **All India Top 10** in **SmashHack '24** <br>
> Secured **All India Top 10** in **Code Sangram '25**

## Overview
This repository is dedicated to the software development of **Luna**, a virtual assistant. The project aims to deliver a seamless and responsive user experience.

## 🛠️ Prerequisites
- Python 3.x (Tested with Python 3.11 using `pyenv`)
- Required Python libraries (listed in `requirements.txt`)

#### Environment Variables
Crank uses a .env file to load sensitive keys and config values. Make sure to create a .env file in the root directory containing your API keys, for example:
```ini
GEMINI_API_KEY=your_api_key_here
```

#### Vosk Model Setup
Crank uses [Vosk](https://alphacephei.com/vosk/) for offline speech recognition. To set it up:
1. **Download an English model** from the official [Vosk models](https://alphacephei.com/vosk/models) page.
2. Recommended model: [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) (~50MB)
3. Extract the model:
```bash
unzip vosk-model-small-en-us-0.15.zip
```
4. Rename the extracted folder to `vosk-model`:
```bash
mv vosk-model-small-en-us-0.15 vosk-model
```
5. **Move it to the project root** so your directory structure looks like:
```
crank/
├── main.py
├── requirements.txt
├── .env
├── vosk-model/
│   ├── conf
│   ├── ... etc
├── other_files_or_dirs/
```

## ⚙️ Installation
1. **Clone the repository**
```bash
git clone https://github.com/ecnivs/Luna.git
cd Blossom
```
2. **Set up Python with `pyenv`**
```bash
pyenv install 3.11
pyenv local 3.11
```
4. **Install dependencies**
```bash
pip install -r requirements.txt
```
5. **Run the Software**
```bash
python main.py
```

## 🙌 Contributing
We appreciate any feedback or code reviews! Feel free to:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Submit a pull request

### I'd appreciate any feedback or code reviews you might have!
