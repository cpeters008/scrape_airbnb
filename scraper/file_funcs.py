import os
import re
import csv
import json
from .message import Message

# Write messages to csv
def write_messages_to_csv(messages, filename='messages.csv'):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    messages_dir = os.path.join(root_dir, 'messages')
    file = os.path.join(messages_dir, filename)

    if not os.path.exists(messages_dir):
        os.makedirs(messages_dir)
    
    file_exists = os.path.isfile(file)

    with open(file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['cid','sender', 'content', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for message in messages:
            writer.writerow({'cid': message.cid, 'sender': message.sender, 'content': message.content, 'timestamp': message.timestamp})

def clean_messages_csv(d, words, filename='messages.csv'):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    messages_dir = os.path.join(root_dir, 'messages')
    file = os.path.join(messages_dir, filename)

    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cleaned_messages = []

        for i, row in enumerate(reader):

            message = Message(row['cid'], row['sender'], row['content'], row['timestamp'])

            # Clean content
            message.clean_content(d, words)
            print(f"Cleaned message {i+1} of {len(reader)}")

            # Add cleaned row to list
            cleaned_messages.append(message)

            # Write to file if the cleaned messages list reaches a certain size
            if len(cleaned_messages) == 100:
                write_messages_to_csv(cleaned_messages, filename='cleaned_messages.csv')
                cleaned_messages = []

        # Write any remaining messages to file
        if len(cleaned_messages) > 0:
            write_messages_to_csv(cleaned_messages, filename='cleaned_messages.csv')

    csvfile.close()

# Write messages to JSON file
def write_messages_to_openai_format_json(messages, filename='messages.json'):
    print("Cleaning messages...")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    messages_dir = os.path.join(root_dir, 'messages')
    file = os.path.join(messages_dir, filename)

    if not os.path.exists(messages_dir):
        os.makedirs(messages_dir)

    data = []

    # Check if the file exists
    if os.path.isfile(file):
        # Load existing data from the file
        with open(file, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

    # Append new messages to the data
    for message in messages:
        data.append(message.to_openai_format())

    # Write the updated data back to the file
    with open(file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)

# Clean messages for openai_json
# Remove phone numbers, email, and correct typos
def clean_messages_openai_json(d, words, filename='messages.json'):
    print("Cleaning messages...")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    messages_dir = os.path.join(root_dir, 'messages')
    file = os.path.join(messages_dir, filename)

    with open(file, 'r', newline='', encoding='utf-8') as jsonfile:
        reader = json.load(jsonfile)
        cleaned_messages = []

        for i, row in enumerate(reader):
            message = Message(0, row['role'], row['content'], 0)

            # Clean content
            message.clean_content(d, words)
            print(f"Cleaned message {i+1} of {len(reader)}")

            # Add cleaned row to list
            cleaned_messages.append(message)

            # Write to file if the cleaned messages list reaches a certain size
            if len(cleaned_messages) == 100:
                write_messages_to_openai_format_json(cleaned_messages, filename='cleaned_messages.json')
                cleaned_messages = []

        # Write any remaining messages to file
        if len(cleaned_messages) > 0:
            write_messages_to_openai_format_json(cleaned_messages, filename='cleaned_messages.json')

    jsonfile.close()