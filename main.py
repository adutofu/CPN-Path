#  making and API calls to Claude making use of PYTHON  # 
"""This following lines of code are for if one want to make use of Anthropic_API_key...
#from dotenv import load_dotenv
#from anthropic import Anthropic
#load_dotenv()
#client = Anthropic()
model = "name of anthropic model that u would like to use"
#reponse = client.messages.create(
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

# import neccessary packages #

from dotenv import load_dotenv

import os # this is because we want to make use of another API key and with out it, (
#which is a function for you to read the other API key in the .env file

from anthropic import Anthropic


from openai import OpenAI

"""creating helper functions that would help to managge conversation better.
in the context of multi-turn conversation"""

#ADD USER MESSAGE FUNCTION
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


#ADD ASSISTANT(AI) MESSAGE FUNCTION
def add_assisntant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)



#now creating the chat function that would make use of the add_user msg and add_assistant msg

def chat(messages):
    message = client.chat.completions.create(
        model = model,
        max_tokens = 1000,
        messages = messages,
    )

    return message.content[0].text


# Load the API KEY from the .env file
load_dotenv()

# Create the client - it automatically reads ANTHROPIC_API_KEY from the environment
client = OpenAI(
    api_key=os.environ.get("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


# select the claude model you would like to use
model = "anthropic/claude-3.5-haiku"


# now making a first request
##############################
response = client.chat.completions.create(
    model = model,
    max_tokens = 1000,
    messages = [
        {"role": "user", "content": "what is devops? Answer in one sentence."}
        ]
)

print('__' * 125)
#print the result
print(response.choices[0].message.content)
print('__' * 125)