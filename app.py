import streamlit as st

from services.stt import GnaniSTTError, transcribe_audio
from services.career_ai import CareerAIError, generate_career_guidance


st.set_page_config(
    page_title="AI Voice Career Assistant",
    page_icon="🎙️"
)

st.title("🎙️ AI Voice Career Assistant")

st.write(
    "Ask about AI careers, learning roadmaps, interview preparation, or resumes."
)


# -----------------------------
# Speech-to-Text
# -----------------------------
st.subheader("🎤 Speech-to-Text")

audio_file = st.file_uploader(
    "Upload an audio recording"
)

if st.button("Transcribe and Get Career Guidance", disabled=audio_file is None):

    try:
        # Step 1: Gnani Speech-to-Text
        transcript = transcribe_audio(
            audio_data=audio_file.getvalue(),
            filename=audio_file.name,
            content_type=audio_file.type or "application/octet-stream",
        )

        st.session_state["stt_transcript"] = transcript

        # Step 2: Gemini Career Guidance
        guidance = generate_career_guidance(transcript)

        st.session_state["career_guidance"] = guidance

    except GnaniSTTError as error:
        st.error(f"Speech-to-Text Error: {error}")

    except CareerAIError as error:
        st.error(f"Career AI Error: {error}")


# -----------------------------
# Display Transcript
# -----------------------------
if "stt_transcript" in st.session_state:

    st.subheader("📝 Your Question")

    st.text_area(
        "Transcript",
        value=st.session_state["stt_transcript"],
        height=120,
    )


# -----------------------------
# Display AI Guidance
# -----------------------------
if "career_guidance" in st.session_state:

    st.subheader("🧠 AI Career Guidance")

    st.write(st.session_state["career_guidance"])


st.caption("Current flow: Audio → Gnani STT → Gemini AI")