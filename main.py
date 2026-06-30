"""IMPORT THE NECCESSARY FUNCTIONS CREATED IN THE CHAT FUNCTION SCRIPT"""


# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat

# IMPORT THE client AND model FROM chat_functions
from chat_functions import client, model

# IMPORT the promt evaluation pipeline functions
from chat_functions import PromptEvaluator, run_prompt


import json





print('__' * 125)
# print the result
# print(response.choices[0].message.content)


# start with an empty message list
messages = []


# get claude response with syestem promt, which allow u to customize the AI response
system = """focus more on professional and dispritive defination. but still
make thing explanatory to understand the concept better."""

add_user_message(messages, "what is devops and diffiferent btween it and full stack developer")

""" .# this is for claude AI sdk streaming
stream = client.messages.create(
model=model,
max_tokens=1000,
messages=messages,
stream=True
)
for event in stream:
print(event)"""

# Anthropic SDK streaming:
# The 'with client.messages.stream' context manager handles the stream lifecycle.
# 'max_tokens' is used to limit the length of the generated response.
# 'messages' contains the conversation history.
# The 'system' prompt also needs to be passed to the streaming call.
full_response = "" # Initialize an empty string to build the full response from the stream.
try:
    with client.messages.stream(
        model=model,
        max_tokens=1000, # Maximum number of tokens to generate in the streamed response.
        messages=messages, # The conversation history for the stream.
        system=system # Pass the system prompt for the streaming call.
    ) as stream:
        # Iterate over each text chunk received from the stream.
        for text_chunk in stream.text_stream:
            print(text_chunk, end="", flush=True) # Print each chunk as it arrives for a real-time effect.
            full_response += text_chunk # Append the chunk to build the complete response.
except Exception as e:
    print(f"\nError during Anthropic streaming API call: {e}")
    full_response = "An error occurred while streaming the response."
    
add_assistant_message(messages, full_response)

print('__' * 125)
# --------add the user second question-----------
add_user_message(messages, "what are the basic project someone can do in regard it")

answer = chat(messages, system=system, temperature=0.8)

print(answer) # you have to use the print function on the first answer gotten, to view it before appending it to messages
add_assistant_message(messages, answer)# ----add claude's response to the conversation histroy---

print('__' * 125)

#----Follow-up question ---------------

# add a follow up question
add_user_message(messages, "in regard the earlier question asked, what is AI engineering")
final_answer = chat(messages)

print(final_answer) # this help u to print the finial response.

print('__' * 125)


# Promt evealuation pipline execution

with open('dataset.json', 'r') as f:
    dataset = json.load(f)

evaluator = PromptEvaluator()
results = evaluator.run_eval(dataset)

print(json.dumps(results, indent=2))