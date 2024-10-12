#!/usr/bin/env python
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParserLocal


loader = GenericLoader(
    FileSystemBlobLoader("input/example.wav", show_progress=True),
    # Lang_model should be a valid model on HugginFace : https://huggingface.co/openai
    OpenAIWhisperParserLocal(lang_model="openai/whisper-large-v3-turbo"),
)
docs = loader.load()

print(docs[0])
