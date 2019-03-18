from bs4 import BeautifulSoup
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from urllib import request
from search.engine.LinkParser import LinkParser
from urllib import parse


class Page:

    def __init__(self, url, html=None, from_page=None):
        self.url = url
        self.parents = set()
        self.document_length = 1
        if from_page is None:
            self.html = html
            html_string = BeautifulSoup(html, 'html.parser')
            self.title = self.get_title()
            self.text = self.get_text(html_string)
            self.links = self.get_links(html_string)
            tokens = self.tokenize(self.text)
            self.vocab = self.make_vocabulary(tokens)
        else:
            self.html = from_page.html
            self.text = from_page.text
            self.links = from_page.links
            self.vocab = from_page.vocab
            self.title = self.get_title()
        self.tfidf = {}
        self.rank = None

    def recalculate_vocab(self):
        tokens = self.tokenize(self.text)
        self.vocab = self.make_vocabulary(tokens)

    def get_text(self, html_string):
        data = html_string.find_all(text=True)
        result = filter(self.visible, data)
        cleaned = [str(item).strip() for item in result]
        cleaned = [item for item in cleaned if item != '']
        return ' '.join(cleaned)

    def get_links(self, html_string):
        parser = LinkParser()
        parser.feed(str(html_string))
        absolutes = [parse.urljoin(self.url, link) for link in parser.links]
        return [link for link in absolutes if 'depaul.edu' in link
                and 'mailto' not in link and link != self.url and '.pdf' not in link and '.jpg' not in link]

    def get_title(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        if soup.title:
            return str(soup.title.string)
        else:
            return self.url

    def transform_vocabulary(self, function):
        for term in self.vocab:
            self.tfidf[term] = function(term, self.vocab[term], self.document_length)

    def normalize(self, function):
        self.document_length = function(self.vocab)

    @staticmethod
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'footer']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    @staticmethod
    def tokenize(text):
        tokens = word_tokenize(text.lower().strip())
        tokens = [w for w in tokens if w not in stopwords.words('english')]
        tokens = [w for w in tokens if w.isalpha()]
        porter = nltk.PorterStemmer()
        tokens = [porter.stem(word) for word in tokens]
        bigrams = []
        for i in range(len(tokens) - 1):
            bigrams.append(tokens[i] + ' ' + tokens[i + 1])
        for bigram in bigrams:
            tokens.append(bigram)
        return tokens

    def make_vocabulary(self, tokens):
        vocab = {}
        for token in tokens:
            n_words = len(token.split(" "))
            if token not in vocab:
                vocab[token] = 0
            weight = 1
            if token in self.title:
                weight = 4
            vocab[token] += weight * n_words
        return vocab

