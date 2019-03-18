from search.engine.TextProcessing import tokenize, make_vocabulary
from spellchecker import SpellChecker
import math

class Query:

    def __init__(self, query):
        self.query = query

    def get_results(self, inv_index, documents):
        query_tokens = tokenize(self.query)
        query_vocab = make_vocabulary(query_tokens)
        return self.rank(query_vocab, inv_index, documents)

    def rank(self, query, inv_index, documents):
        R = dict()
        ssq = 0.0
        for token in query:
            if token not in inv_index:
                continue
            i = len(inv_index[token])  # IDF of token
            k = query[token]  # Frequency of token in query
            w = i * k  # TF-IDF for T in Q
            ssq += w ** 2  # Increment sum of squares

            postings = inv_index[token]
            for document in postings:
                c = documents[document].vocab[token]
                if document not in R:
                    R[document] = 0.0
                R[document] += (w * c * i)

        L = math.sqrt(ssq)
        for document in R:
            S = R[document]
            Y = documents[document].document_length
            R[document] = .5*(S / (L * Y)) + .5*documents[document].rank
            # R[document] = S / (L * Y)

        return sorted(R.items(), key=lambda x: x[1], reverse=True)
