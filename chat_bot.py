# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat

# IMPORT THE client & model from the CHAT_FUNCTION
from chat_functions import client,  model


# get claude response with system promt, which allow u to customize the AI response
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

    # Add the assistant's streamed response to the conversation history
    add_assistant_message(messages, full_response)

    print("\n")
    # The full_response already contains the assistant's answer from the stream.
    # No need for a separate chat() call here, as it would be redundant and costly.
    # print("Stored message:", full_response) # Optional: print the stored message for debugging.
