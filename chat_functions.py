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

from statistics import mean

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
model = "claude-haiku-20231024-5" # Using Claude Haiku 4.5 as a capable and cost-effective option.



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
        "temperature": temperature, # Controls the randomness of the model's output. Higher values mean more random.
        "stop_sequences": stop_sequences,
         
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


# CREATING OF THE GRADER FUNCTION & we are making use of a model grader, THAT WOULD BE USED IN THE run_eval function
def grade_by_model(test_case, output):
    # This function implements the 'LLM-as-a-judge' pattern.
    # It leverages a highly capable model to act as an expert reviewer,
    # providing structured feedback and a numerical score for the AI's output.
    
    # 1. Define a detailed evaluation prompt using XML-like tags to clearly 
    # delineate the original task from the AI-generated solution.
    eval_prompt = f"""
you are and expert AWS code reviewr. your task is to evaluate the following AI_generated solution.

Original Task:
<task>
{test_case["task"]}
</task>

AI Generated Solution:
<solution>
{output}
</solution>

Output Format
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}
    """

    # 2. Build the message history for the evaluation request.
    messages = []
    add_user_message(messages, eval_prompt)
    
    # 3. Use 'pre-filling' to force the assistant to start with a JSON block.
    # This significantly improves reliability by ensuring the response begins with data.
    add_assistant_message(messages, "```json")
    
    # 4. Call the LLM and use a stop sequence to halt generation at the end of the JSON block.
    eval_text = chat(messages, stop_sequences=["```"])
    
    # 5. Deserialize the JSON string into a structured Python dictionary.
    return json.loads(eval_text)





def run_eval(dataset):
    """
    Evaluates a set of test cases by running each one and collecting the results.

    Args:
        dataset (list): A list of dictionaries, where each dictionary represents a test case.

    Returns:
        list: A list of dictionaries, each containing the output, original test case, and score
              for a given test case.
    """
    results = []
    # Iterate through each test case in the provided dataset.
    for test_case in dataset:
        # Execute the test case and get its result (output and score).
        result = run_test_case(test_case)
        # Append the result of the current test case to the results list.
        results.append(result)
    return results


# FUNCTION TO EXECUTE A SINGLE TEST CASE AND GRADE THE OUTPUT
def run_test_case(test_case):
    """
    Executes a single test case by calling the AI with the prompt and then grades the response.

    Args:
        test_case (dict): A dictionary representing a single test case, typically containing a "task".

    Returns:
        dict: A dictionary containing the AI's output, the original test case, and its assigned score.
    """
    # Call the run_prompt function to get the AI's response for the given test case.
    output = run_prompt(test_case)

    # TODO - replace with real grading logic
    # Currently, a placeholder score of 10 is assigned. This should be replaced
    # with actual logic to evaluate the 'output' against expected criteria.
    score = model_grade["score"]

    # Perform the "LLM-as-a-judge" evaluation using the grader function.
    # This replaces the hardcoded placeholder with dynamic AI evaluation.
    model_grade = grade_by_model(test_case, output)
    reasoning = model_grade["reasoning"]

    return {
        "output": output,
        "test_case": test_case, # Corrected typo from "tast_case" to "test_case".
        "score": score,
        "test_case": test_case,
        "reasoning": reasoning
    }

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
