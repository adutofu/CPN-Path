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

import json

from anthropic import Anthropic # Import the Anthropic client for interacting with Anthropic models.


# Load the API KEY from the .env file
load_dotenv()

# Create the Anthropic client - it automatically reads ANTHROPIC_API_KEY from the environment.
# Ensure you have ANTHROPIC_API_KEY set in your .env file.
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"), # Anthropic client automatically looks for ANTHROPIC_API_KEY.
)


# select the claude model you would like to use
# Using a specific Anthropic model identifier.
# Examples: "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"
# For the latest models, check Anthropic's documentation.
model = "claude-3-5-sonnet-20240620" # Using Claude 3.5 Sonnet as a capable and cost-effective option.



# ADD USER MESSAGE FUNCTION THIS CAN ALSO WORK FOR ANTHROPIC AND OTHER AI
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)



# ADD ASSISTANT(AI) MESSAGE FUNCTION THIS CAN ALSO WORK FOR ANTHROPIC AND OTHE AI
def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


# NOW CREATING THE CHAT FUNCTION THAT WOULD MAKE USE OF THE ADD_MSG and ADD_ASSISTANT MSG..

# THIS IS THE ADAPTED CHAT FUNCTION FOR ANTHROPIC SDK
def chat(messages, system=None, temperature=1.0, stop_sequences=None):
    # Anthropic's messages API expects a 'system' parameter for system prompts,
    # separate from the 'messages' list which contains user/assistant turns.
    # If a system prompt is provided, it will be passed directly to the 'system' parameter.
    
    # Anthropic uses 'max_tokens' to limit the length of the generated response.
    # The 'stop_sequences' parameter is directly supported by Anthropic.
    
    # Create the parameters dictionary for the Anthropic API call.
    params = {
        "model": model, # The specific Anthropic model to use.
        "max_tokens": 1000, # Maximum number of tokens to generate in the response.
        "messages": messages, # The conversation history, a list of message dictionaries.
        "temperature": temperature # Controls the randomness of the model's output. Higher values mean more random.
    }

    # If a system prompt is provided, add it to the parameters.
    if system:
        params["system"] = system # Anthropic's API takes a dedicated 'system' parameter.

    # If stop sequences are provided, add them to the parameters.
    if stop_sequences:
        params["stop_sequences"] = stop_sequences # Anthropic uses 'stop_sequences' parameter.

    try:
        # Make the API call to Anthropic.
        message = client.messages.create(**params)
        # Anthropic returns a list of content blocks. 
        # We need to access the text field of the first block.
        return message.content[0].text
    except Exception as e:
        print(f"Error during Anthropic API call: {e}")
        # Return None so calling functions know the generation failed.
        return None


# Dataset generating function for prompt evaluation
def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []

    # Append the structured instructions (the prompt variable) to the messages list as a 'user' role input.
    add_user_message(messages, prompt)

    # Inject a pre-filled assistant response to guide the model's generation.
    # By forcing the model to start with "```json", it ensures the AI begins outputting the raw data array directly
    # instead of wasting tokens on conversational text like "Sure, here is your dataset:".
    add_assistant_message(messages, "```json") # Standardizing to triple backticks for JSON block.

    # Send the messages payload to the LLM. The 'stop_sequences' parameter tells the model to stop generating
    # immediately when it outputs the closing triple backticks ("```"), preventing extra text trailing at the end.
    text = chat(messages, stop_sequences=["```"]) # Corrected stop sequence to triple backticks.

    if text is None:
        print("Failed to generate dataset due to API error.")
        return []
    
    # Strip away any leading or trailing whitespace or hidden newline characters from the model's string response.
    text = text.strip()
    
    if text.endswith('```'):
        text = text[:-3].strip()

    # Print the final cleaned-up JSON string to the console/terminal.
    print(text)

    # Convert the generated text into a json file and rename it to the variable data
    # then return the valrable data to the function
    return json.loads(text)
    
# Defines the `run_prompt` function, which merges a generic prompt with a specific test case.
# This function is designed to send a task to the AI and retrieve its solution.
def run_prompt(test_case):
    """
    Constructs a prompt for the AI based on a given test case and retrieves the AI's response.

    Args:
        test_case (dict): A dictionary containing details of the task, typically with a "task" key.

    Returns:
        str: The AI's generated response to the task.
    """
    # Formulate the prompt by embedding the test case's task description.
    prompt = f"""
please solve the following task:

{test_case["task"]}
"""
    # Initialize an empty list to hold the conversation messages for this specific interaction.
    messages = []
    # Add the constructed prompt as a user message to the conversation history.
    add_user_message(messages, prompt)
    # Send the messages to the AI model and get its response.
    output = chat(messages)
    # Return the AI's output.
    return output
