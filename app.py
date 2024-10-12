#!/usr/bin/env python
# External imports
import streamlit as st
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParserLocal
# Internal imports
from src.helpers.file_uploader import file_uploader
from src.helpers.config import *

st.title("🎥 MoMify Video")

"""
In this app, you can upload a video in order to extract text transcription then create a MoM from it.
This application is running locally (no external services called) and uses under the hood : 
- Whisper to transcript video ;
- LangChain as the glue ;
- Mistral as the LLM engine ;

You can try it out directly, or have a look at the source code here : [github.com/ThomasVuillaume/langchain-transcript](https://github.com/ThomasVuillaume/langchain-transcript).
"""

st.subheader("Video Input", divider=True)
uploaded_file = st.file_uploader("Upload the video to process.", type=("mkv", "mp4"))

if uploaded_file:
    uploaded_file_name = file_uploader.save_uploaded_file(uploaded_file)
    st.success(f"File {uploaded_file_name} saved successfully")
    loader = GenericLoader(
        FileSystemBlobLoader(f"{CONF_SAVE_DIR}/{uploaded_file_name}", show_progress=True),
        OpenAIWhisperParserLocal(lang_model=CONF_WHISPER_MODEL)
    )
    with st.spinner('Extracting audio and writing transcript...'):
        docs = loader.load()
        st.subheader("Raw Transcript", divider=True)
        for record in docs:
            st.write(record.page_content)
        st.balloons()