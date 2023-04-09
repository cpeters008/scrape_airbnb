# message_parser.py
import re
import spacy
from datetime import datetime
from message import Message
from nameparser import HumanName

def parse_messages(raw_text, cid):
    messages = []
    message_pattern = re.compile(r"(\w+)\s+sent\s+(.+)\. Sent (\w+ \d{1,2}, \d{4}, \d{1,2}:\d{2} [AP]M)")

    for match in message_pattern.finditer(raw_text):
        sender = match.group(1)
        content = match.group(2).strip()
        timestamp = datetime.strptime(match.group(3), "%b %d, %Y, %I:%M %p")
        messages.append(Message(cid, sender, content, timestamp))

    return messages

def remove_emails(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[email]', text)

def remove_phone_numbers(text):
    return re.sub(r'\+?\d[\d -]{7,}\d', '[phone]', text)

def remove_names(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            text = text.replace(ent.text, '[name]')
    return text

def correct_typos(text):
    # Assuming you have a function for correcting typos, you can use it here
    return text

def clean_content(text):
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_names(text)
    text = correct_typos(text)
    return text
