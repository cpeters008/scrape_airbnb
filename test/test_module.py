import os
import sys
import shutil
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.message import Message
from scraper.file_funcs import *

class TestMessage(unittest.TestCase):

    def test_clean_content(self):
        # Test case 1: content contains PII (personally identifiable information)
        message = Message("cid", "sender", "My phone number is 123-456-7890", "timestamp")
        expected_clean_content = "My phone number is [phone]"
        print(f"Original content: {message.content}")
        message.remove_phone_numbers()
        print(f"Cleaned content: {message.content}")
        self.assertEqual(message.content, expected_clean_content)

        # Test case 2: content contains typos
        message = Message("cid", "sender", "Helo, how are you?", "timestamp")
        expected_clean_content = "Hello, how are you?"
        print(f"Original content: {message.content}")
        message.correct_typos()
        print(f"Cleaned content: {message.content}")
        self.assertEqual(message.content, expected_clean_content)

        # Test case 3: content contains person names
        message = Message("cid", "sender", "Hello Chad, how are you?", "timestamp")
        expected_clean_content = "Hello [name], how are you?"
        print(f"Original content: {message.content}")
        message.remove_names()
        print(f"Cleaned content: {message.content}")
        self.assertEqual(message.content, expected_clean_content)

        # Test case 4: content contains emails 
        message = Message("cid", "sender", "my email is abc@gmail.com", "timestamp")
        expected_clean_content = "my email is [email]"
        print(f"Original content: {message.content}")
        message.remove_emails()
        print(f"Cleaned content: {message.content}")
        self.assertEqual(message.content, expected_clean_content)

        # Test case 5: content is already clean
        message = Message("cid", "sender", "Hello, how are you?", "timestamp")
        expected_clean_content = "Hello, how are you?"
        print(f"Original content: {message.content}")
        message.clean_content()
        print(f"Cleaned content: {message.content}")
        self.assertEqual(message.content, expected_clean_content)
        return None

    def setUp(self):
        self.messages = [
            Message(1, 'John', 'Hello World!', '2022-04-09 16:30:00'),
            Message(2, 'Mary', 'How are you?', '2022-04-09 16:31:00'),
            Message(3, 'John', 'I am fine, thank you', '2022-04-09 16:32:00')
        ]

    def test_write_messages_to_csv(self):
        root_dir = '../scraper'
        messages_dir = os.path.join(root_dir, 'messages')
        filename = 'messages.csv'
        file = os.path.join(messages_dir, filename)

        # Write messages to csv
        write_messages_to_csv(self.messages)

        # Check if the file was created
        self.assertTrue(os.path.isfile(file))

        # Read messages from csv and check if they are correct
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                if self.messages[i].cid == 'cid':
                    continue
                self.assertEqual(int(row['cid']), int(self.messages[i].cid))
                self.assertEqual(row['sender'], self.messages[i].sender)
                self.assertEqual(row['content'], self.messages[i].content)
                self.assertEqual(row['timestamp'], self.messages[i].timestamp)

        # Clean up     
        shutil.rmtree(messages_dir)

    def test_write_messages_to_openai_format_json(self):
        root_dir = '../scraper'
        messages_dir = os.path.join(root_dir, 'messages')
        filename = 'messages.json'
        file = os.path.join(messages_dir, filename)

        # Write messages to json
        write_messages_to_openai_format_json(self.messages)

        # Check if the file was created
        self.assertTrue(os.path.isfile(file))

        # Read messages from json and check if they are correct
        with open(file, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for i, message in enumerate(self.messages):
                self.assertEqual(data[i]['role'], 'user')
                self.assertEqual(data[i]['content'], message.content)

        # Clean up     
        shutil.rmtree(messages_dir)