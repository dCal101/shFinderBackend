from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.generativeai as genai
import os

# Blueprint for the Gemini API middleware
gemini_middleware = Blueprint('gemini_middleware', __name__)

# Scopes required for the Gemini API
SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever',
          'https://www.googleapis.com/auth/generative-language.tuning']

def load_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

@gemini_middleware.route('/gemini-api/', methods=['POST'])
@cross_origin()
def gemini_api():
        if request.method == "POST":
            data = request.get_json()
            query = data["query"]
        
        creds = load_creds()
        genai.configure(credentials=creds)

        return jsonify({"response": "what good bro"})

        tuned_model_name = "tunedModels/shfindermedium-kfim1ju3r0fx"
        tuned_model = genai.get_tuned_model(tuned_model_name)

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "response_mime_type": "text/plain",
        }

        safety_settings = {
            "HATE_SPEECH": "BLOCK_LOW_AND_ABOVE",
            "HARASSMENT": "BLOCK_LOW_AND_ABOVE",
            "SEXUALLY_EXPLICIT": "BLOCK_LOW_AND_ABOVE",
            "DANGEROUS_CONTENT": "BLOCK_LOW_AND_ABOVE",
        }

        model = genai.GenerativeModel(
            model_name=tuned_model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        data = request.get_json()
        hobbies = data.get("query")

        question = '''
        Hi! I'm really interested in finding a side hustle that is unique in that it has low competition. It should be scalable and not that hard to start/learn based on my unique skills and hobbies. 

IMPORTANT: 
You don't have to use all of my unique skills, but at least one. If it doesn't make sense to use more than 1, don't force it. Only do so if it makes a practical idea.

Think about how to find a unique, not straight-forward side hustle by breaking down my interests, finding unique business ideas that can be scaled to sell to other people, and which has a niche, untapped market waiting for that idea.



Find really unique ideas to talk about. Here is an example of an idea that has helped other people based on their relevant skills:

{
Example 1:

User: I’m organized, and I’m an immigrant who loves my culture.

Your thinking process: The user is an immigrant, so that means they have come from another country and adapted to their current country. Find what aspects of this are difficult yet have low untapped solutions. This means not looking at immigrants in a direct manner, but about issues that are not directly visible.Be motivated by any direction of any soft skills present in the user skill input. Further, be sure to look in the direction of a relevant niche market. For example, for this case, this could be about the moving process in particular which requires lots of organizational skills. Then see how you could take this further by finding problems that are faced by many people in a niche market and think of solutions that would be highly effective yet not a straight-forward idea. 
  In this example, note that in the moving process, items may be thrown away when moving yet needed in a new country. See how these items can be gotten cheaply in their new countries. They could get these items from people who may be throwing away unwanted items. The user’s organizational skills would be great to start a decluttering business that could connect citizens’ unwanted items with immigrants who needed items at cheap price.

}

Example of something that doesn't work:


{
 User: I’m a fitness freak, and I love taking care of my fish

Bad answer:

Thinking Process:
Given your interests in fitness and taking care of fish, I'll break down how these could lead to unique side hustle opportunities. Both of these areas have passionate communities, but to find a niche market that is scalable and has low competition, I'll focus on:

Fitness Enthusiasm: The fitness market is large and competitive, so finding a unique angle is key. Consider intersections with technology, personalized coaching, or unconventional methods.

Aquarium/Fish Care: The fish care industry, while niche, has devoted enthusiasts who invest heavily in their hobby. Exploring the care, customization, and aesthetics of aquariums could open up unique business opportunities.

Idea: Customized Fitness Routines for People with Unique Hobbies
Concept:
Create and market highly customized fitness routines for people with niche hobbies, such as aquarium enthusiasts. The routines could be designed to improve aspects of their hobby, such as strength for lifting tanks, posture for prolonged sitting during aquascaping, or even stress-relief exercises to complement the relaxing nature of aquarium maintenance.

Why is this BAD? Because fitness with fish tanks is too much of a stretch that other people would obviously not use in their fitness routines. This is an example of something where merging the two would not make sense.

}

Common examples include connecting people over a unique hobby, or using a cultural twist to an otherwise 
After you think of an idea, be sure to talk about the concept, scalability, and the specific, untapped niche market that you are addressing, all in depth. Show your thinking process.

Here are my unique skills/hobbies:

Cooking (BBQ), Blogging
   
''' + hobbies

        response = model.generate_content(question)
        response_text = response.candidates[0].text

        return jsonify({"response": response_text})

    
