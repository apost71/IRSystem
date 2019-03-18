from search.engine.InvertedIndex import InvertedIndex
from search.engine.Page import Page
from urllib.parse import urlparse
import pickle
import sys

def remove_duplicates(documents):
    print(len(documents))
    cleaned_documents = {}
    removed = []
    for url in list(documents):
        if url in removed:
            continue
        parsed = urlparse(url)
        for other in list(documents):
            other_parsed = urlparse(other)
            parsed_host = parsed.netloc
            other_host = other_parsed.netloc
            if 'www.' in parsed_host:
                parsed_host = parsed_host.split('www.')[1]
            if 'www.' in other_host:
                other_host = other_host.split('www.')[1]
            if parsed.scheme != other_parsed.scheme and parsed_host == other_host and parsed.path == other_parsed.path and parsed.params == other_parsed.params and parsed.query == other_parsed.query:
                print('{} == {}'.format(url, other))
                removed.append(other)
            elif parsed_host == other_host and parsed.path == other_parsed.path and parsed.params == other_parsed.params and parsed.query == other_parsed.query and parsed.fragment != other_parsed.fragment:
                print('{} == {}'.format(url, other))
                removed.append(other)
            else:
                cleaned_documents[url] = documents[url]
    print(len(removed))
    print(len(cleaned_documents))
    return cleaned_documents

def set_parents(documents):
    print('setting parents...')
    for document in documents:
        documents[document].parents = set()

    for url in documents:
        page = documents[url]
        for child in page.links:
            if child in documents:
                child_page = documents[child]
                child_page.parents.add(url)

    return documents

def replace_pages(documents):
    print('replacing pages...')
    print(len(documents))
    i = 0
    for document in documents:
        page = documents[document]
        new_page = Page(document, from_page=page)
        print('count: {} url: {}'.format(i, new_page.url))
        i += 1
        documents[document] = new_page
    print('finished replacing pages')

    return documents

if __name__ == "__main__":
    sys.path.append("search/engine/")
    # inv_index = pickle.load(open('data/inv_index.p', 'rb')) # dictionary with inverted index
    documents = pickle.load(open('data/pages_new_test.p', 'rb')) # dictionary with key: url_string and value: Page object
    index = InvertedIndex(documents)
    index.tf_idf()
    #
    # documents = remove_duplicates(documents)
    documents = set_parents(documents)
    documents = replace_pages(documents)

    pickle.dump(documents, open('data/pages1.p', 'wb'))