#!/usr/bin/env python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.helpers.prompts import en_extract_MoM
from src.helpers.config import CONF_OLLAMA_MODEL, CONF_OLLAMA_HOST

# Initialize Ollama ChatModel with the desired model
model = ChatOllama(
    model=CONF_OLLAMA_MODEL,
    base_url=CONF_OLLAMA_HOST,
    # other params...
)

# Init parser
parser = StrOutputParser()


def extract_mom_from(transcript, output_langague):
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", en_extract_MoM.PROMPT), ("human", "{input}")]
    )

    # Create the chain
    chain = prompt_template | model | parser
    stream = chain.stream({"input": transcript, "language": output_langague})
    return stream
