import sys
sys.path.append('../PyFiles/')
import DescriptionCollect
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate



def create_llm():
    load_dotenv()
    genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))
    llm = GoogleGenerativeAI(model='gemini-pro', temperature=True, convert_system_message_to_human=True)
    
    return llm


def return_hookline(tweet_url):
    llm = create_llm()
    description = DescriptionCollect.get_description(tweet_url)
    
    prompt_string = "Given the following text enclosed by triple backticks, please remove any special characters or emojis, and then \
                        provide a concise summary, in 25 words or less, that captures the main idea of the text: \
                        ```{text}```. Please provide the cleaned text summarized in a short, concise and hooking manner. \
                        It should be easy to understand for non-ai domain people too. Please dont include * or doublequotes in the output \
                    "


    prompt_template = ChatPromptTemplate.from_template(template=prompt_string)
    
    prompt = prompt_template.format_messages(text=description)
    
    hookline = llm.invoke(prompt)
    
    return hookline




