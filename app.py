import streamlit as st
import os

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Create a directory to save uploaded files if it doesn't exist
        save_dir = "uploaded_files"
        # Save the file
        file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return f"File {uploaded_file.name} saved successfully"
    return "No file uploaded"

st.title("🎥 LangChain Video Transcriptor")

"""
In this app, you can upload a video in order to extract text transcription and summary from it.
This application is running locally (no external services called) and uses under the hood : 
- Whisper to transcript video ;
- LangChain as the glue ;
- Mistral as the LLM engine ;

You can try it out directly, or have a look at the source code here : [github.com/ThomasVuillaume/langchain-transcript](https://github.com/ThomasVuillaume/langchain-transcript).
"""

uploaded_file = st.file_uploader("Upload the video to process.", type=("mkv", "mp4"))

if uploaded_file:
    result = save_uploaded_file(uploaded_file)
    st.write("### Uploaded")
    st.success(result)