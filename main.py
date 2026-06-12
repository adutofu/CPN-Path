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

response = client.chat.completions.create(
    model = model,
    max_tokens = 1000,
    messages = [
        {"role": "user", "content": "what is devops? Answer in one sentence."}
        ]
)


print(response.choices[0].message.content)