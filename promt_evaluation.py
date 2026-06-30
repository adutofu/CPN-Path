"""
This script handles the creation of a local evaluation dataset by prompting
the AI to generate a list of AWS-related programming tasks.
"""

import json

# Import chat management and messaging functions from the helper module
from chat_functions import add_user_message, add_assistant_message, chat
from chat_functions import client, model, generate_dataset
from chat_functions import PromptEvaluator

# Optionally generate a new dataset:
# dataset = generate_dataset()
# with open('dataset.json', 'w') as f:
#     json.dump(dataset, f, indent=2)

with open("dataset.json", "r") as f:
    dataset = json.load(f)

evaluator = PromptEvaluator()
results = evaluator.run_eval(dataset)

print(json.dumps(results, indent=2))