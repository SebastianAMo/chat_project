import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)


import json
from models.contact import Contact
from models.message import Message

def contact_to_json(contact):
    return json.dumps(contact.__dict__)

def json_to_contact(data):
    obj = json.loads(data)
    return Contact(obj['ip'], obj['port'], obj['label'])

def message_to_json(message):
    return json.dumps(message.__dict__)

def json_to_message(data):
    obj = json.loads(data)
    return Message(obj['sender'], obj['content'])
