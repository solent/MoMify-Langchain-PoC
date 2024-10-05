from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def main():
    # Initialize the Ollama LLM with the Mistral model
    llm = Ollama(model="mistral")

    # Create a prompt template
    prompt = PromptTemplate(
        input_variables=["question"],
        template="Human: {question}\nAI:",
    )

    # Create an LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain
    response = chain.invoke("Hello, how are you?")

    print("AI's response:")
    print(response)

if __name__ == "__main__":
    main()