from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import math


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


def make_vocabulary(tokens):
    vocab = {}
    for token in tokens:
        n_words = len(token.split(" "))
        if token not in vocab:
            vocab[token] = 0
        vocab[token] += 1*n_words
    return vocab


def tf_idf(self):
    for url in self.pages:
        page = self.pages[url]
        for term in page.vocab:
            if term not in self.df:
                self.df[term] = 0
            self.df[term] += 1
    for url in self.pages:
        page = self.pages[url]
        page.transform_vocabulary(self.ltc)
        page.normalize(self.cosine_normalization)
        # print(page.vocab)
        # print(page.weight)


def ltc(raw_value, n_docs, df):
    return (1 + math.log(raw_value, 2)) * math.log(n_docs / df)


def cosine_normalization(vocab):
    sum = 0.0
    for term in vocab:
        sum += vocab[term] ** 2
    return 1 / math.sqrt(sum)
