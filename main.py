import logging
import os
from display_cost_and_summary import display_summary_and_cost
from dotenv import load_dotenv
from langchain_community.llms import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from openai import OpenAI
from langchain.callbacks.openai_info import OpenAICallbackHandler

load_dotenv()
llm = OpenAI()
llmLang=openai.OpenAI(callbacks=[OpenAICallbackHandler()])
template = """Question: {question} Answer: Let's explore."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llmLang)


logging.basicConfig(filename="log.log", filemode="w", level=logging.INFO)
logger = logging.getLogger(__name__)


def transcribe_audio(audio_file_path: str) -> str:
    logger.info(f"transcribe audio {audio_file_path}")
    with open(audio_file_path, "rb") as audio_file:
        transcript = llm.audio.transcriptions.create(
            file=audio_file, model="whisper-1", response_format="text", language="en"
        )

    with open("transcription.txt", "w") as f:
        f.write(transcript)

    return transcript

def abstract_summary_extraction(transcription):
    question = "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could  help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points." + transcription
    output = llm_chain.run(question)
    return output

def key_points_extraction(transcription):
    question = "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about." + transcription
    output = llm_chain.run(question)
    return output

def action_items_extraction(transcription):
    question = "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely." + transcription
    output = llm_chain.run(question)
    return output

def sentiment_analysis(transcription):
    question = "As an AI with expertise in language ad emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible." + transcription
    output = llm_chain.run(question)
    return output

def call_recording_minutes(transcription):
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription)
    action_items = action_items_extraction(transcription)
    sentiment = sentiment_analysis(transcription)

    return {
        "abstract_summary": abstract_summary,
        "key_points": key_points,
        "action_items": action_items,
        "sentiment": sentiment,
    }


def save_to_md(call_recording_dict, file_name):
    with open(file_name, "w") as file:
        file.write("# Calling Minutes\n\n")
        file.write("## Abstract Summary\n\n")
        file.write(f"{call_recording_dict['abstract_summary']}\n\n")
        file.write("## Key Points\n\n")
        file.write(f"{call_recording_dict['key_points']}\n\n")
        file.write("## Action Items\n\n")
        file.write(f"{call_recording_dict['action_items']}\n\n")
        file.write("## Sentiment Analysis\n\n")
        file.write(f"{call_recording_dict['sentiment']}\n\n")

def call_recording_main():
    dir_path = "audio"
    for filename in os.listdir(dir_path):
        logger.info(f"Starting Summarizing calls {filename}")
    transcription = transcribe_audio(f"{dir_path}/{filename}")
    data = call_recording_minutes(transcription)
    filename = filename.split(".")[0]
    file = f"audio_summary/{filename}_call_recording_summary_of_.md"
    save_to_md(data, file)
    response_from_callback = llmLang.callbacks
    display_summary_and_cost(file, response_from_callback)