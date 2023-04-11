# message.py
import re
import spacy
import string
import Levenshtein as lev
import nltk
from nameparser import HumanName

class Message:
    def __init__(self, cid, sender, content, timestamp):
        self.cid = cid
        self.sender = sender
        self.content = content
        self.timestamp = timestamp

    def __repr__(self):
        return f"Message(cid='{self.cid}', sender='{self.sender}', content='{self.content}', timestamp='{self.timestamp}')"

    def to_openai_format(self):
            if self.sender not in ['Terri', 'Chad', 'Sari']:
                 self.sender = 'user'
            else:
                 self.sender = 'assistant'
            return {
                'role': self.sender,
                'content': self.content
            }
    
    # def remove_emails(self):
    #     self.content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[email]', self.content)

    # def remove_phone_numbers(self):
    #     self.content = re.sub(r'(\+?\d{1,3}?\s*(?:-|\.)?\s*)?(\(?\d{2,3}\)?|\d{2,3})(?:\s*|-|\.)?\d{2,4}(?:\s*|-|\.)?\d{2,4}', '[phone]', self.content)

    # def remove_names(self):
    #     nlp = spacy.load('en_core_web_sm')
    #     doc = nlp(self.content)
    #     for ent in doc.ents:
    #         if ent.label_ == 'PERSON':
    #             # Use nameparser to parse out first and last names
    #             name = HumanName(ent.text)
    #             first_name = name.first
    #             last_name = name.last
    #             if first_name:
    #                 # Remove first name from content
    #                 self.content = re.sub(r'\b{}\b'.format(first_name), '[name]', self.content)
    #             if last_name:
    #                 # Remove last name from content
    #                 self.content = re.sub(r'\b{}\b'.format(last_name), '[name]', self.content)

    def correct_typos(self, d, words):
        # Tokenize the content
        tokens = nltk.wordpunct_tokenize(self.content)

        # Tag the tokens with POS
        tagged_tokens = nltk.pos_tag(tokens)

        # Correct typos using pyenchant
        corrected_tokens = []
        orig_tokens = []
        for i, (token, pos) in enumerate(tagged_tokens):
            if pos.startswith('N') and token.lower() not in words:
                # Don't correct proper nouns
                corrected_tokens.append(token)
                orig_tokens.append((token, i))
            elif not d.check(token):
                # Correct typos
                suggestions = d.suggest(token)
                if suggestions:
                    distances = [lev.distance(token, sugg) for sugg in suggestions]
                    best_match = suggestions[distances.index(min(distances))]
                    corrected_tokens.append(best_match)
                else:
                    corrected_tokens.append(token)
                orig_tokens.append((token, i))
            else:
                corrected_tokens.append(token)
                orig_tokens.append((token, i))

        # Add back punctuation
        for i, (token, idx) in enumerate(orig_tokens):
            if i > 0 and idx > orig_tokens[i-1][1]+1:
                orig_tokens[i] = (token, idx+i-1)
            elif idx == orig_tokens[0][1]:
                orig_tokens[0] = (token, idx+len(token))

        # Join the corrected tokens back into a string
        corrected_str = []
        for i, (token, ws) in enumerate(corrected_tokens):
            if len(ws) < 2:
                corrected_str.append(token)
            else:
                corrected_str.append(''.join(ws[:-1]) + token)
            if i < len(corrected_tokens) - 1:
                corrected_str.append(self.content[orig_tokens[i][1]+1:orig_tokens[i+1][1]])
        self.content = ''.join(corrected_str)


    # Clean data for analysis
    def clean_content(self, d, words):
        self.correct_typos(d,words)
