# message.py
from datetime import datetime

class Message:
    def __init__(self, cid, sender, content, timestamp):
        self.cid = cid
        self.sender = sender
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return f"Message(conversationId='{self.cid}', sender='{self.sender}', content='{self.content}', timestamp='{self.timestamp}')"

    def to_openai_format(self):
            if self.sender not in ['Terri', 'Chad', 'Sari']:
                 self.sender = 'user'
            else:
                 self.sender = 'assistant'
            return {
                'role': self.sender,
                'content': self.content
            }

