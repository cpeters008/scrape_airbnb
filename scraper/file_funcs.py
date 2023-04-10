import os
import csv
import json

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

# Write messages to JSON file
def write_messages_to_openai_format_json(messages, filename='messages.json'):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    messages_dir = os.path.join(root_dir, 'messages')
    file = os.path.join(messages_dir, filename)

    if not os.path.exists(messages_dir):
        os.makedirs(messages_dir)

    data = []

    # Check if the file exists
    if os.path.isfile(file):
        # Load existing data from the file
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

    # Append new messages to the data
    for message in messages:
        data.append(message.to_openai_format())

    # Write the updated data back to the file
    with open(file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)
