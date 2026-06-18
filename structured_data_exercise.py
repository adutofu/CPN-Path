# Import the function to add a user message to the conversation history
from chat_functions import add_user_message

# Import the function to add an assistant (AI) message to the conversation history
from chat_functions import add_assistant_message

# Import the main chat function that sends messages to the AI model and returns a response
from chat_functions import chat

# Import the OpenAI client and the model identifier used for making API calls
from chat_functions import client, model


# Initialize an empty list to hold the conversation messages
messages = []

# Define the prompt that tells the AI what to generate
# In this case, we ask for three short sample AWS CLI commands
prompt = """
Generate three diffrent sample AWS CLI commands. Each should be very short.
"""

# Add the user's prompt to the conversation history
add_user_message(messages, prompt)

# Add an assistant message that starts a JSON code block
# This primes the AI to output its response in JSON format
add_assistant_message(messages, "```json") # Standardizing to triple backticks for JSON block.


# Send the conversation to the AI model and get the response
# The stop_sequences parameter tells the AI to stop generating when it reaches "```"
text = chat(messages, stop_sequences=["```"]) # Corrected stop sequence to triple backticks.

if text:
    # Remove any leading/trailing whitespace from the response
    text = text.strip()
    # Print the generated AWS CLI commands to the console
    print(text)
else:
    print("Error: Could not retrieve a response from the AI. Please check your API credits or connection.")