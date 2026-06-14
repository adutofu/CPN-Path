"""IMPORT THE NECCESSARY FUNCTIONS CREATED IN THE CHAT FUNCTION SCRIPT"""


# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat


print('__' * 125)
# print the result
# print(response.choices[0].message.content)


# start with an empty message list
messages = []

# add the initial user question
add_user_message(messages, "what is devops and diffiferent btween it and full stack developer")

# get claude haiku response, without syestem promt
answer = chat(messages)


# get claude response with syestem promt, which allow u to customize the AI response
system = """focus more on professional and dispritive defination. but still
make thing explanatory to understand the concept better."""

answer = chat(messages, system=system)

print(answer) # you have to use the print function on the first answer gotten, to view it before appending it to messages

print('__' * 125)

# add claude's response to the conversation histroy
add_assistant_message(messages, answer)

# add a follow up question
add_user_message(messages, "in regard the earlier question asked, what is AI engineering")
final_answer = chat(messages)

print(final_answer) # this help u to print the finial response.

print('__' * 125)
