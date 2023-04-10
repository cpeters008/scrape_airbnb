# message.py
import re
import spacy
import string
import enchant
import nltk
import Levenshtein as lev
from nltk.corpus import brown
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.metrics.distance import edit_distance
from textblob import TextBlob

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
    
    def remove_emails(self):
        self.content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[email]', self.content)

    def remove_phone_numbers(self):
        self.content = re.sub(r'(\+?\d{1,3}?\s*(?:-|\.)?\s*)?(\(?\d{2,3}\)?|\d{2,3})(?:\s*|-|\.)?\d{2,4}(?:\s*|-|\.)?\d{2,4}', '[phone]', self.content)

    def remove_names(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.content)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                self.content = self.content.replace(ent.text, '[name]')

    def correct_typos(self):
        if not nltk.data.find('corpora/brown'):
            nltk.download('brown')
        if not nltk.data.find('taggers/averaged_perceptron_tagger'):
            nltk.download('averaged_perceptron_tagger')
        if not nltk.data.find('tokenizers/punkt'):
            nltk.download('punkt')

        # Load the Brown corpus and create a list of words
        words = set(brown.words())
        words.update(nltk.corpus.words.words())

        d = enchant.Dict("en_US")

        # Tokenize the content
        tokens = word_tokenize(self.content)

        # Correct typos using TextBlob and pyenchant
        corrected_tokens = []
        for i, token in enumerate(tokens):
            if token.isalpha() and not d.check(token):
                suggestions = d.suggest(token)
                if suggestions:
                    distances = [lev.distance(token, sugg) for sugg in suggestions]
                    best_match = suggestions[distances.index(min(distances))]
                    corrected_tokens.append(best_match)
                else:
                    corrected_tokens.append(token)
            else:
                corrected_tokens.append(token)

        # Join the corrected tokens back into a string
        self.content = ''.join([' ' + token if not token.startswith("'") and token not in string.punctuation else token for token in corrected_tokens]).strip()

            
    # Clean data for analysis
    def clean_content(self):
        self.remove_emails()
        self.remove_phone_numbers()
        self.remove_names()
        self.correct_typos()
