"""Creating helper functions that would help to manage conversation better.
in the context of multi-turn conversation"""


"""This following lines of code are for if one want to make use of Anthropic_API_key...
from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()
client = Anthropic()
model = "name of anthropic model that u would like to use"
reponse = client.messages.create(
    model=model
    max_tokens=1000
    messages=[
    {
    "role": "user",
    "content": "what is devops?"
    }
]
)

print(response.content[0].text)
"""

# import neccessary packages

from dotenv import load_dotenv

import os # this is because we want to make use of another API key
#which is a function for you to read the other API key in the .env file


from openai import OpenAI


# Load the API KEY from the .env file
load_dotenv()

# Create the client - it automatically reads ANTHROPIC_API_KEY from the environment
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


# select the claude model you would like to use
model = "anthropic/claude-3.5-haiku"



# ADD USER MESSAGE FUNCTION THIS CAN ALSO WORK FOR ANTHROPIC AND OTHER AI
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)



# ADD ASSISTANT(AI) MESSAGE FUNCTION THIS CAN ALSO WORK FOR ANTHROPIC AND OTHE AI
def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


# NOW CREATING THE CHAT FUNCTION THAT WOULD MAKE USE OF THE ADD_MSG and ADD_ASSISTANT MSG..

"""THIS line, is specific to Athropic
def chat(messages):
    message = client.messages.create(
    model = model
    max_tokens = 1000
    messages = messages)
    
    return message.content[0].text"""


# THIS WORKS FOR ONLY OPENROUTER AI
def chat(messages, system=None, temperature=1.0):
    if system:
        messages = [{"role": "system", "content": system}] + messages
    
    params = { 
            "model": model,
            "max_tokens" : 1000,
            "messages" : messages,
            "temperature" : temperature
    }  
    
    message = client.chat.completions.create(**params)

    
    return message.choices[0].message.content

