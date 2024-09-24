import os 
from dotenv import load_dotenv, dotenv_values 
import google.generativeai as genai

load_dotenv() 

def regularCall(query, chatHistory):

    key = os.getenv('API_KEY')

    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    safety_settings={
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_LOW_AND_ABOVE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_LOW_AND_ABOVE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_LOW_AND_ABOVE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_LOW_AND_ABOVE'
    }
    chat = model.start_chat(
        history = chatHistory
    )
    confg = genai.GenerationConfig(
        temperature = 1.0
    )
    response = chat.send_message(
        query,
        safety_settings = safety_settings,
        generation_config = confg
        )

    return response.text
#x = regularCall(query = "How many paws do I have in total?")
#print(x)


