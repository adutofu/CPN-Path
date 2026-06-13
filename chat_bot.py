# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat

# start with an empty message list
messages = []



# Now make use of a while loop, this keeps the chat bot active untill u interrupt it

while True:
    
    # This takes string of input from the user
    user_input = input("> ")
    
    # This line stops the while loop and the chatbot
    if user_input.lower() in ["exit" or "quit"]:
        break

    add_user_message(messages, user_input)

    # get AI response with chat function

    answer = chat(messages)

    # add the answer to the list of generated text
    add_assistant_message(messages, answer)


    print('____')
    print(answer)
    print('____')






