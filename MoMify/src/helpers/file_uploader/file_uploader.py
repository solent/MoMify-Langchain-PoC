import os
from src.helpers.config import CONF_SAVE_DIR


def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Save the file
        file_path = os.path.join(CONF_SAVE_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return uploaded_file.name
    return "No file uploaded"
