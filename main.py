"""IMPORT THE NECCESSARY FUNCTIONS CREATED IN THE CHAT FUNCTION SCRIPT"""


# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat

# IMPORT THE client AND model FROM chat_functions
from chat_functions import client, model


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

# ---this works only for openrouter sdk setup---
stream = client.chat.completions.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    stream=True
)
full_response =""

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end="", flush=True)
        full_response += content
    
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




