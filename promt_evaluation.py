"""
This script handles the creation of a local evaluation dataset by prompting
the AI to generate a list of AWS-related programming tasks.
"""

# Import chat management and messaging functions from the helper module
from chat_functions import add_user_message
from chat_functions import add_assistant_message
from chat_functions import chat
# Import connection configuration and the main generation function
from chat_functions import client, model
from chat_functions import generate_dataset
from chat_functions import run_eval
from chat_functions import run_test_case
from chat_functions import run_prompt
from statistics import mean


import json

# Execute the dataset generation.
# This function handles the LLM request and returns a parsed JSON list.
dataset = generate_dataset()

# Persist the dataset to a local JSON file. 
# Storing the tasks allows for repeatable evaluation without re-generating data.
#with open('dataset.json', 'w') as f:
    #json.dump(dataset, f, indent=2)



with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)

print(json.dumps(results, indent=2))