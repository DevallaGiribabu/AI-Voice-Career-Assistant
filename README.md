# AI-Voice-Career-Assistant

A voice career assistant with a static web interface and Python serverless
functions for Vercel, plus the original Streamlit app in `app.py`. It
transcribes uploaded audio with Gnani Speech-to-Text, then generates career
guidance with Google Gemini. Text-to-Speech is not connected.

## Deploy to Vercel

1. Import `DevallaGiribabu/AI-Voice-Career-Assistant` into your Vercel account.
2. Set `GNANI_API_KEY` and `GEMINI_API_KEY` in the Vercel project's
   **Settings > Environment Variables**. Use Production (and Preview if
   desired), then redeploy.
3. Keep these values in Vercel only; never commit them or put them in the
   browser code.

Vercel serves `index.html` and deploys the Python functions in `api/`.
`vercel.json` sets a 60-second function duration. Audio uploads are limited
to 4 MiB to fit within the serverless request-body limit.

## Run locally

Install the Python dependencies, then run `streamlit run app.py` for the
original Streamlit interface. To test the Vercel interface locally, install
the Vercel CLI and run `vercel dev` from the project directory.

Set `GNANI_API_KEY` and `GEMINI_API_KEY` in your local environment, or copy
`.env.example` to `.env` and fill in the values. `.env` files are ignored by
Git.

## Services

- `api/transcribe.py` accepts an audio upload and calls the Gnani STT service.
- `api/guidance.py` accepts the transcript and calls Gemini
  `gemini-3.5-flash-lite`.
- `services/` contains the Gnani and Gemini service clients.
