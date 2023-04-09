import os
import csv
import json

# Write messages to csv
def write_messages_to_csv(messages, filename='./messages/messages.csv'):
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['cid','sender', 'content', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for message in messages:
            writer.writerow({'cid': message.cid, 'sender': message.sender, 'content': message.content, 'timestamp': message.timestamp})

# Write messages to JSON file
def write_messages_to_openai_format_json(messages, filename='./messages/messages.json'):
    data = []

    # Check if the file exists
    if os.path.isfile(filename):
        # Load existing data from the file
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)

    # Append new messages to the data
    for message in messages:
        data.append(message.to_openai_format())

    # Write the updated data back to the file
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)
