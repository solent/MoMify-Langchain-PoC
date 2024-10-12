#!/usr/bin/env python
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize Ollama ChatModel with the desired model
model = ChatOllama(
    model="llama3.2",
    temperature=0.9,
    # other params...
)

parser = StrOutputParser()

# Create a prompt template
with open('../data.txt', 'r') as file:
    data = file.read().replace('\n', '')
system_template = """
You're an experienced translator.
Translate the following into {language}.
Does not output anything else than the translated text. Here is the text to translate:"""

prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('human', '{input}')
])

# Create the chain
chain = prompt_template | model | parser
