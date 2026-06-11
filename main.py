#  making and API calls to Claude making use of PYTHON  # 


# import neccessary packages #

from dotenv import load_dotenv
from anthropic import Anthropic

# Load the API KEY from the .env file
load_dotenv()

# Create the client - it automatically reads ANTHROPIC_API_KEY from the environment
client = Anthropic()


# select the claude model you would like to use
model = "claude-haiku-4.5"


# now making a first request

response = client.messages.create(
    model = model,
    max_tokens = 1000,
    messages = [
        {"role": "user", "content": "what is devops? Answer in one sentence."}
        ]
)


print(response.content[0].text)