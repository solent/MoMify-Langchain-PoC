#!/usr/bin/env python
# External imports
import streamlit as st
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParserLocal

# Internal imports
from src.helpers.file_uploader import file_uploader
from src.helpers.config import CONF_SAVE_DIR, CONF_WHISPER_MODEL
from src.helpers.ollama import chat_ollama

st.title("🎥 MoMify Video")

"""
In this app, you can upload a video in order to extract text transcription then create a MoM from it.
This application is running locally (no external services called) and uses under the hood : 
- Whisper to transcript video ;
- LangChain as the glue ;
- Ollama as the LLM engine ;
"""

st.subheader("Video Input", divider=True)
uploaded_file = st.file_uploader("Upload the video to process.", type=("mkv", "mp4"))
output_langague = st.selectbox(
    "In what language do you want the MoM to be outputed?",
    ("Please select a language", "French", "English", "Spanish"),
)

if uploaded_file and output_langague != "Please select a language":
    uploaded_file_name = file_uploader.save_uploaded_file(uploaded_file)
    st.success(f"File {uploaded_file_name} saved successfully")
    with st.spinner("Loading Whisper Model..."):
        st.write(
            f"Whisper model {CONF_WHISPER_MODEL} is being loaded. It can take some time. ☕"
        )
        st.write(
            "PS: At first start, it will be downloaded to disk, taking also a bit of time. 😒"
        )
        loader = GenericLoader(
            FileSystemBlobLoader(
                f"{CONF_SAVE_DIR}/{uploaded_file_name}", show_progress=True
            ),
            OpenAIWhisperParserLocal(lang_model=CONF_WHISPER_MODEL),
        )
    st.subheader("Raw Transcript", divider=True)
    with st.spinner("Extracting audio and writing transcript..."):
        docs = loader.load()
        st.success(
            f"File {uploaded_file_name} transcripted successfully! Here's the transcript:"
        )
        raw_transcript = ""
        for record in docs:
            raw_transcript += record.page_content
            st.write(record.page_content)
        st.download_button("Download raw transcript", raw_transcript)

    st.subheader("MoM Extraction", divider=True)
    with st.spinner("Extracting MoM..."):
        stream_data = chat_ollama.extract_mom_from(raw_transcript, output_langague)
        st.success(f"Here's the MoM, in {output_langague}, as requested:")
        extracted_mom = st.write_stream(stream_data)
        st.download_button("Download MoM", extracted_mom)

    st.balloons()
