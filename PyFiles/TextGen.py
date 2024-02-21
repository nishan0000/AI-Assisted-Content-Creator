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
    llm = GoogleGenerativeAI(model='gemini-pro', temperature=0, convert_system_message_to_human=True)
    
    return llm

def collect_description_for_ai(tweet_url):
    description = DescriptionCollect.get_description(tweet_url)
    return description

def return_hookline(description):
    llm = create_llm()
    
    
    prompt_string = "Given the following text enclosed by triple backticks, please remove any special characters or emojis, and then \
                        provide a concise summary, in 25 words or less, that captures the main idea of the text: \
                        ```{text}```. Please provide the cleaned text summarized in a short, concise and hooking manner. \
                        It should be easy to understand for non-ai domain people too. return it as string. not a markdown \
                    "
    prompt_template = ChatPromptTemplate.from_template(template=prompt_string)
    
    prompt = prompt_template.format_messages(text=description[1])
    
    hookline = llm.invoke(prompt)
    
    return hookline

def return_caption(description):
    llm = create_llm()
    
    cap_prompt_string = """
        Act as an article writing expert that has expertise in writing using simple words and user friendly words, 
        so write me a good 2 long sentenced article after doing your own research about the topic and from the 
        relevant sources gather the best information about it and include that as well that is for this topic


            The topic of the post is : {text}


        write the article in a descriptive way but in a neutral tone such that a normal guy is talking about it in 
        two or three good sentences, make sure it is having atleast 35 words in it , Make sure that the paragraph is 
        in good and simple words and also have a neutral tone and try to add a question for people to engage in the 
        comments if possible, also include 5 simple hashtags at the very end for instagram relevant to the topic and 
        single word hashtags, and write this before the hashtags as well.


        I want the whole output in this format, only take the format from this below example


        example : [
            The future is here  Apple’s Vision Pro has finally gone on sale, allowing the first customers to 
            get their hands on the $3,500 computer.

            The augmented reality headset – called a “spatial computer” by Apple – was 
            launched last year. 

            The company suggested that it marks not only a major new product category for 
            Apple but a whole new form of computing.

            Credits to haig98/X & @sanjosefoos

            Follow @bardotics for more AI related updates!
        ]

        After creating the text, make sure this is included in the end of your output. There will not be any improvisation in this.
        The text below should be fixed. and even the order of it.



        (First place this) : Credits to @{username}

        (Second place this) : Follow @bardotics for more such content!

        (Third place this) : #hashtag1 #hashtag2 #hashtag3 #hashtag4 #hashtag5 



        You have to make sure about these things :

        1. you leave the SPACES RIGHT between all the sentences and after the sentences as well, leave a line or two after 
        the sentences to match the formatting in the example
        2. dont add emojis, 
        3. leave the space blank where the username has to be given by me, 
        4. also make sure there are 35 or more words in the paragraph
        5. make sure you add good latest and relevant information about it and provide the reader with a valuable time 
        that is used for reading this article
        6. If necessary you can add an extra paragraph too, depending on the depth of the topic
        7. Dont add unnecessary intro texts to begin, start directly talking about the topic
        8. Make sure the formatting is right and the 'Follow @bardotics' line is included at all times
        """

    cap_prompt_template = ChatPromptTemplate.from_template(template=cap_prompt_string)

    cap_prompt = cap_prompt_template.format_messages(text=description[1], username=description[0])
    
    caption = llm.invoke(cap_prompt)
    
    return caption

def generate_text_using_ai(tweet_url):
    description = collect_description_for_ai(tweet_url)
    hookline = return_hookline(description)
    caption = return_caption(description)
    return hookline, caption

