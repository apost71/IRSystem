import math
import pickle

class InvertedIndex:

    def __init__(self, pages, inv_index=None):
        self.pages = pages
        if inv_index is None:
            self.inv_index = {}
            for url in self.pages:
                for term in self.pages[url].vocab:
                    if term not in self.inv_index:
                        self.inv_index[term] = set()
                    self.inv_index[term].add(url)
        else:
            self.inv_index = inv_index
        self.df = {}

    def tf_idf(self):
        for url in self.pages:
            page = self.pages[url]
            for term in page.vocab:
                if term not in self.df:
                    self.df[term] = 0
                self.df[term] += 1
        for url in self.pages:
            page = self.pages[url]
            page.normalize(self.cosine_normalization)
            page.transform_vocabulary(self.ltc)

    def ltc(self, term, raw_value, document_length):
        return (1+math.log(raw_value, 2)) * math.log(len(self.df) / self.df[term]) * (1/document_length)

    def cosine_normalization(self, vocab):
        sum = 0.0
        if vocab == {}:
            return 0
        for term in vocab:
            sum += vocab[term]**2
        return math.sqrt(sum)

    def serialize(self):
        pickle.dump(self.inv_index, open('data/inv_index.p', 'wb'))

