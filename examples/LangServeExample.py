#!/usr/bin/env python
from fastapi import FastAPI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

# Initialize Ollama ChatModel with the desired model
model = ChatOllama(
    model="llama3.2",
    temperature=0.9,
    # other params...
)

parser = StrOutputParser()

# Create a prompt template
system_template = """
You're an experienced translator.
Translate the following into {language}.
Does not output anything else than the translated text. Here is the text to translate:"""

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("human", "{input}")]
)

# Create the chain
chain = prompt_template | model | parser

# App definition
app = FastAPI(
    title="LangChain Translator Example",
    version="1.0",
    description="A simple API server using LangChain's runnable interfaces",
)

# Adding chain route
add_routes(
    app,
    chain,
    path="/translator",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
