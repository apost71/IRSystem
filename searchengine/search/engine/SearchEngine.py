import pickle
from search.engine.Query import Query
from search.engine.InvertedIndex import InvertedIndex
from search.engine.Page import Page
from spellchecker import SpellChecker
from search.engine.UpdateIndex import set_parents, replace_pages
import datetime
import sys


class SearchEngine:

    def __init__(self):
        sys.path.append("search/engine/")
        print('initializing search engine...')
        self.documents = pickle.load(open('search/engine/data/pages.p', 'rb'))
        # self.replace_pages()
        # pickle.dump(self.documents, open('search/engine/data/pages.p', 'wb'))
        self.index = InvertedIndex(self.documents)
        self.index.tf_idf()
        self.compute_page_rank()

    def replace_pages(self):
        i = 0
        for document in self.documents:
            self.documents[document] = Page(document, from_page=self.documents[document])
            self.documents[document].recalculate_vocab()
            if i % 100 == 0:
                print('Finished replacing page {} out of {}'.format(i, len(self.documents)))
            i += 1

    def query(self, query_string):
        query = Query(query_string)
        results = query.get_results(self.index.inv_index, self.documents)
        return [self.documents[doc[0]] for doc in results[:20]]

    def compute_page_rank(self, alpha=0.15):
        initial_rank = 1 / len(self.documents)
        for document in self.documents:
            page = self.documents[document]
            page.rank = initial_rank

        converged = False
        while not converged:
            previous_ranks = {}
            new_ranks = self.iterate_ranks(previous_ranks, alpha)
            avg_diff = self.diff(new_ranks, previous_ranks)
            if abs(avg_diff) < 0.000000001:
                converged = True

    def iterate_ranks(self, ranks, alpha):
        new_ranks = {}
        for document in self.documents:
            ranks[document] = self.documents[document].rank
        for document in self.documents:
            page = self.documents[document]
            parents = page.parents
            parents_ranks = [ranks[doc] / len(self.documents[doc].links) for doc in parents]
            page.rank = sum(parents_ranks) + alpha / len(self.documents)
            self.documents[document] = page
            new_ranks[document] = page.rank
        return new_ranks

    def diff(self, current_ranks, previous_ranks):
        diff = 0.0
        for document in current_ranks:
            diff += (current_ranks[document] - previous_ranks[document])
        return diff / len(current_ranks)

    @staticmethod
    def spell_check(phrase):
        spell = SpellChecker()
        terms = [x.strip() for x in phrase.split(" ")]
        misspelled = spell.unknown(terms)
        for i in range(len(terms)):
            if terms[i] in misspelled:
                terms[i] = spell.correction(terms[i])
        return ' '.join(terms)


if __name__ == "__main__":
    sys.path.append("search/engine/")
    # inv_index = pickle.load(open('data/inv_index.p', 'rb')) # dictionary with inverted index
    # documents = pickle.load(open('data/pages.p', 'rb')) # dictionary with key: url_string and value: Page object
    # index = InvertedIndex(documents)
    # index.tf_idf()

    engine = SearchEngine()
    pickle.dump(engine.documents, open('data/pages1.p', 'wb'))

    # compute_page_rank(documents)
    #
    # while True:
    #     query_string = input('Query: ')
    #     query = Query(query_string)
    #     start = datetime.datetime.now()
    #     results = query.get_results(index.inv_index, documents)
    #     print('Retrieved {} results in {}s'.format(len(results), datetime.datetime.now() - start))
    #     for result in results[:20]:
    #         print(result)