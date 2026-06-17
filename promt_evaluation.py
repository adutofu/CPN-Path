# IMPORT THE add_user_message FUNCTION
from chat_functions import add_user_message

# IMPORT THE add_assistant_message FUNCTION
from chat_functions import add_assistant_message

# IMPORT THE chat FUNCTION
from chat_functions import chat

# IMPORT THE client & model from the CHAT_FUNCTION
from chat_functions import client,  model

from chat_functions import generate_dataset

import json

dataset = generate_dataset()
#print(dataset)

with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)


