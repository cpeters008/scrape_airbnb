# message_parser.py
import re

from datetime import datetime
from .message import Message

def parse_messages(raw_text, cid):
    messages = []
    message_pattern = re.compile(r"(\w+)\s+sent\s+(.+)\. Sent (\w+ \d{1,2}, \d{4}, \d{1,2}:\d{2} [AP]M)")

    for match in message_pattern.finditer(raw_text):
        sender = match.group(1)
        content = match.group(2).strip()
        timestamp = datetime.strptime(match.group(3), "%b %d, %Y, %I:%M %p")
        message = Message(cid, sender, content, timestamp)
        messages.append(message)

    return messages
