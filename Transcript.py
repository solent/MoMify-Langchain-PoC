import os
import logging
from typing import Dict, Any, Union

import ffmpeg
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from langchain.llms import Ollama
from langchain.schema import AgentAction, AgentFinish
from pydantic import BaseModel, Field

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure Whisper.cpp is installed and set up
try:
    import whisper_cpp
except ImportError:
    logger.error("Whisper.cpp is not installed. Please install it following the instructions at https://github.com/ggerganov/whisper.cpp")
    exit(1)

class WhisperTranscriptionTool(BaseModel):
    name: str = "Whisper Transcription"
    description: str = "Transcribes audio using Whisper.cpp"
    
    def _call(self, audio_path: str) -> str:
        try:
            model = whisper_cpp.WhisperModel("path/to/whisper/model.bin")
            segments = model.transcribe(audio_path)
            return " ".join([segment.text for segment in segments])
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            return ""

    def run(self, audio_path: str) -> str:
        return self._call(audio_path)

def extract_audio(video_path: str, output_path: str) -> str:
    try:
        (
            ffmpeg
            .input(video_path)
            .output(output_path, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        logger.error(f"Error extracting audio: {str(e)}")
        return ""

class TranscriptionInput(BaseModel):
    video_path: str = Field(description="Path to the .mkv video file")

class TranscriptionAgent(LLMSingleActionAgent):
    tools: list
    llm_chain: LLMChain

    class Config:
        arbitrary_types_allowed = True

    @property
    def input_keys(self):
        return ["input"]

    def plan(self, intermediate_steps: list, **kwargs: Any) -> Union[AgentAction, AgentFinish]:
        return self.llm_chain.predict(intermediate_steps=intermediate_steps, **kwargs)

    def aplan(self, intermediate_steps: list, **kwargs: Any) -> Union[AgentAction, AgentFinish]:
        return self.llm_chain.apredict(intermediate_steps=intermediate_steps, **kwargs)

class CustomPromptTemplate(StringPromptTemplate):
    template: str
    tools: list

    def format(self, **kwargs) -> str:
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += f"Action: {action.tool}\nAction Input: {action.tool_input}\nObservation: {observation}\n"
        kwargs["agent_scratchpad"] = thoughts
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)

def create_transcription_agent(tools):
    prompt = CustomPromptTemplate(
        template="""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}""",
        tools=tools,
        input_variables=["input", "intermediate_steps"]
    )

    # Initialize Ollama with the Mistral model
    llm = Ollama(model="mistral")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    tool_names = [tool.name for tool in tools]
    agent = TranscriptionAgent(tools=tools, llm_chain=llm_chain)
    return AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

def main():
    whisper_tool = WhisperTranscriptionTool()
    tools = [
        Tool(
            name="Extract Audio",
            func=lambda x: extract_audio(x, "temp_audio.wav"),
            description="Extracts audio from an .mkv video file"
        ),
        Tool(
            name=whisper_tool.name,
            func=whisper_tool.run,
            description=whisper_tool.description
        )
    ]

    agent = create_transcription_agent(tools)

    video_path = input("Enter the path to the .mkv video file: ")
    result = agent.run(TranscriptionInput(video_path=video_path))
    print(f"Transcription: {result}")

if __name__ == "__main__":
    main()