import json

class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

    def to_json(self):
        return json.dumps({
            'sender': self.sender,
            'content': self.content
        })

def message_from_json(json_str):
    data = json.loads(json_str)
    return Message(data['sender'], data['content'])
