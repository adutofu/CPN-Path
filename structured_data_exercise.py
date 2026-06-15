from chat_functions import add_user_message

from chat_functions import add_assistant_message


from chat_functions import chat

from chat_functions import client, model


messages = []

prompt = """
Generate three diffrent sample AWS CLI commands. Each should be very short.
"""

add_user_message(messages, prompt)


text = chat(messages)
text = text.strip()

print(text)