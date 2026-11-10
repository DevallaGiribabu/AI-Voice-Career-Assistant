# AI-Voice-Career-Assistant

A Streamlit voice career assistant that transcribes uploaded audio with Gnani
Speech-to-Text and generates career guidance with Google Gemini. Text-to-Speech
is not connected yet.

## Setup on Windows

```powershell
cd "C:\path\to\ai-voice-career-assistant"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Copy `.env.example` to `.env` and add your Gnani and Gemini API keys:

```text
GNANI_API_KEY=your_gnani_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

`.env` is ignored by Git. Never put API keys in application code or commit them.

## Services

- `services/stt.py` transcribes uploaded audio with the Gnani STT API.
- `services/career_ai.py` generates career guidance using the Gemini
  `gemini-3.5-flash-lite` model.
- The current flow is audio upload -> transcription -> career guidance. TTS is
  a future addition.
