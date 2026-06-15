# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat

# IMPORT THE client & model from the CHAT_FUNCTION
from chat_functions import client,  model


# get claude response with syestem promt, which allow u to customize the AI response
# we start by defining the system varabile
    
system = """focus more on professional and dispritive defination. but still
make thing explanatory to understand the concept better."""

# start with an empty message list
messages = []

print("Chatbot is ready. Type 'exit' to stop")


"""This is for getting complete stream message with Athropic SDK in the context of this chat_bot
it should be indented into the while loop.
with client.messages.stream(
model=model,
max_tokens=1000,
messages=messages
) as stream:
for text in stream.text_stream:
# Send each chunk to your client
pass
# Get the complete assembled message
final_message = stream.get_final_message()"""




# Now make use of a while loop, this keeps the chat bot active untill u interrupt it

while True:
    
    # This takes string of input from the user
    user_input = input("> ")
    
    # This line stops the while loop and the chatbot
    if user_input.lower() in ["exit", "quit"]:
        break

    add_user_message(messages, user_input)

    # For getting complete stream msg with OpenRouter. it has no .stream() content manager or .text_stream
    # You filter chunks mannually instead
    stream = client.chat.completions.create(
        model = model,
        max_tokens = 1000,
        messages = messages,
        stream = True
    )
    full_response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
        full_response += content

    # Add the assistant's streamed response to the conversation history
    add_assistant_message(messages, full_response)

    print("\n")
    print("stored message:", full_response)

   
    

    answer = chat(messages, system=system, temperature=0.0)


    # add the answer to the list of generated text
    add_assistant_message(messages, answer)


    print('____')
    print(answer)
    print('____')






