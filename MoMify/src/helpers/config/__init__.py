# Model should be a valid model on HugginFace : https://huggingface.co/openai
CONF_WHISPER_MODEL = "openai/whisper-large-v3-turbo"  # "openai/whisper-tiny"
# Ollama Model should be among the supported ones : https://ollama.com/library
CONF_OLLAMA_MODEL = "llama3.2"
# If you use docker-compose, use the service hostname : http://ollama:11434 otherwise localhost:11434
CONF_OLLAMA_HOST = "http://ollama:11434"
# Upload file folder
CONF_SAVE_DIR = "MoMify/data/uploaded_files"
