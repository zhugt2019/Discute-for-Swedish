# 👋 Discute for Swedish Language Beginners!

This application is based on Discute, an open-source language learning tool, and now offers improved support for the Swedish language. Users can practice and perfect their Swedish speaking skills by simulating realistic conversations with AI.

## 🚀 Features

- **Context Generation**: Input a situation or automatically generate a real-life Swedish dialogue context.  
- **LLM-powered Conversation**: AI responds in Swedish, playing a role based on the context and conversation history.  
- **Language Coach Review**: Get a CEFR-level assessment, major error corrections, and concise improvement suggestions.  
- **User-Friendly Interface**: Intuitive and accessible UI built with Streamlit.

## 🛠️ Technologies Used

- Python
- Google Gemini for language models
- Streamlit for the UI framework
- KBLab/kb-whisper-small for Swedish STT
- Facebook/mms-tts-swe for Swedish TTS
- FFmpeg for external audio processing

## 📦 Setup and Installation

To get "Discute" running locally:

1. Clone the repository: `git clone https://github.com/zhugt2019/Discute-for-Swedish.git`
2. Change directory: `cd Discute`
3. Install required dependencies: `pip install -r requirements.txt`
4. Install FFmpeg, and add it to the environment variable
5. Obtain a Gemini API key (available for free under the “free tier”)
6. Set the API key as an environment variable
7. Run the Streamlit application: `streamlit run app.py`
8. It might take a while for the models to be downloaded to a cache directory on first run

## 🧩 System Requirements

- Python 3.8 or higher
- Minimum 4GB RAM (8GB recommended)
- NVIDIA GPU with CUDA support (highly recommended)
- Stable internet connection for AI models
- Working microphone for voice input

## Happy learning!
