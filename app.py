import streamlit as st
import os

from main import transcribe_audio, generate_response, generate_audio
from prompt_managements import pm

# TTS: Massively Multilingual Speech (MMS): Swedish Text-to-Speech
# https://huggingface.co/facebook/mms-tts-swe

DEFAULT_VOICE = "swedish_mms_voice" 

# Gemini model names:
# https://ai.google.dev/gemini-api/docs/models?hl=zh-cn
MODEL_CONTEXT = "gemini-1.5-flash"
MODEL_CHAT = "gemini-1.5-flash"

VOICES = {
        "Swedish Voice": "swedish_mms_voice" # Only one option for now
}

def init_session_state() -> None:
    """Initialize session state variables if they don't exist"""
    if "context" not in st.session_state:
        st.session_state.context = ""
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "voice" not in st.session_state:
        st.session_state.voice = DEFAULT_VOICE

def display_chat_history() -> None:
    """Display the chat history with audio playback and detailed timing logs."""
    for msg in st.session_state.chat:
        with st.container(border=True):
            role_label = "**Me**" if msg["role"] == "me" else "**Assistant**"
            st.write(role_label)
            st.audio(msg["audio"], format="audio/wav")
            with st.expander("Show Details", expanded=False):
                st.write(f"**Message:** {msg['content']}")
                
                # Display detailed LLM timing
                if "llm_log" in msg and msg["llm_log"]:
                    st.write("**LLM Generation Time Details:**")
                    for step, duration in msg["llm_log"].items():
                        st.write(f"- {step.replace('_', ' ').capitalize()}: {duration:.2f} 秒")
                
                # Display detailed TTS timing
                if "tts_log" in msg and msg["tts_log"]:
                    st.write("**TTS Generation Time Details:**")
                    for step, duration in msg["tts_log"].items():
                        st.write(f"- {step.replace('_', ' ').capitalize()}: {duration:.2f} 秒")

def format_chat_history() -> str:
    """Format the chat history for prompt context"""
    return "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in st.session_state.chat
    )

def generate_context(prompt: str) -> None:
    context_text, _ = generate_response(prompt, MODEL_CONTEXT)
    st.session_state.context = context_text
def main():
    """Main application function"""
    st.write("# Discute")
    st.caption("A demo application for chatting with an AI assistant")

    init_session_state()

    col1, col2 = st.columns(2, border=True)

    with col1:
        st.write("**Context Prompt**")
        situation = st.text_input("Context", placeholder="Describe the situation (in any language)")
        context_prompt = pm.get_prompt("context_prompt", variables={"Situation": situation})

        if st.button("Generate Context Prompt"):
            generate_context(context_prompt)

    with col2:
        st.write("**Random Context Generation**")

        if st.button("Generate Random Context", use_container_width=True):
            generate_context(pm.get_prompt("random_context"))

    if st.session_state.context:
        st.write("**Context:**")
        st.info(st.session_state.context)

    st.write("**Voice Selection**")
    st.write(f"Currently using: **{list(VOICES.keys())[0]}** (MMS-TTS Swedish Model)")
    st.session_state.voice = DEFAULT_VOICE

    display_chat_history()

    audio_col, btn_col = st.columns([3, 1])

    with audio_col:
        audio_value = st.audio_input("Record voice message in Swedish")

    with btn_col:
        st.write("")
        st.write("")
        st.write("")
        if st.button("Send", use_container_width=True):
            if not audio_value:
                st.error("Please record a voice message before sending")
            else:
                # Process user audio
                audio_bytes = audio_value.read()
                text = transcribe_audio(audio_bytes)
                st.session_state.chat.append({"role": "me", "content": text, "audio": audio_bytes})

                # Generate AI response and capture detailed LLM log
                chat_history = format_chat_history()
                prompt_vars = {
                        "Context": st.session_state.context,
                        "ChatHistory": chat_history
                }

                chat_prompt = pm.get_prompt("chat_prompt", variables=prompt_vars)
                ai_response, llm_detailed_log = generate_response(chat_prompt, MODEL_CHAT)

                # Generate audio for AI response and capture detailed TTS log
                audio_data, tts_detailed_log = generate_audio(ai_response, st.session_state.voice)

                # Add to chat history, including detailed timing logs
                st.session_state.chat.append({
                        "role": "you",
                        "content": ai_response,
                        "audio": audio_data,
                        "llm_log": llm_detailed_log, # Store detailed LLM log
                        "tts_log": tts_detailed_log  # Store detailed TTS log
                })
                st.rerun()

    st.write("**AI Coach Review**")

    if st.button("Review and Correct", use_container_width=True):
        if not st.session_state.chat:
            st.error("No conversation yet to review")
        else:
            conversation = format_chat_history()
            coach_vars = {
                    "context": st.session_state.context,
                    "conversation": conversation
            }

            coach_prompt = pm.get_prompt("swedish_coach", variables=coach_vars)
            review, _ = generate_response(coach_prompt, MODEL_CHAT)

            st.write("**Coach Review:**")
            st.info(review)

if __name__ == "__main__":
    main()
