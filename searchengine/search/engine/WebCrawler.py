from search.engine.Page import Page
from search.engine.InvertedIndex import InvertedIndex
from collections import deque
import pickle
import ssl
from urllib import request
from urllib.error import HTTPError
import time
from urllib.parse import urlparse
import sys


class WebCrawler:

    def __init__(self, start):
        self.queue = deque()
        self.queue.append(start)
        self.visited = {}
        self.exclusions = self.find_exclusions(start)
        self.urls = set()

    def find_exclusions(self, start):
        context = ssl.SSLContext()
        response = request.urlopen(start + 'robots.txt', context=context)
        text = response.read().decode('utf-8')
        lines = text.split('\r\n')
        exclude = []
        for line in lines:
            if 'Disallow' in line:
                path = line.split(' ')[1]
                exclude.append(path)
        return exclude


    def crawl(self, n_iter):
        context = ssl.SSLContext()
        iter = len(self.visited)
        while iter < n_iter and self.queue:
            url = self.queue.popleft()
            print('Building page {} for: {}'.format(iter, url))
            if not self.update(url, context):
                continue
            iter += 1
            time.sleep(1)
            if len(self.visited) % 100 == 0:
                self.set_parents()
                self.serialize()
        for page in self.visited:
            print(sorted(self.visited[page].vocab.items(), key=lambda kv: kv[1], reverse=True))
        self.set_parents()
        for page in self.visited:
            print('url: {} parents: {}'.format(self.visited[page].url, self.visited[page].parents))

    def validate(self, url):
        if url in self.visited:
            return False

        parsed = urlparse(url)
        host = parsed.netloc

        if not parsed.fragment:
            if 'www.' in parsed.netloc:
                host = parsed.netloc.split('www.')[1]
            path = host + parsed.path + parsed.params + parsed.query
            if path not in self.urls:
                self.urls.add(path)
                return True
            else:
                print('Not adding {} with url: {}'.format(path, url))
                return False
        else:
            print('Appending {} to the beginning of the queue'.format(parsed.scheme + '://' + parsed.netloc + parsed.path + parsed.params + parsed.query))
            self.queue.appendleft(parsed.scheme + '://' + parsed.netloc + parsed.path + parsed.params + parsed.query)
            return False

    def update(self, url, context):
        if not self.validate(url):
            return False

        html = self.get_response(url, context)
        if not html:
            return False

        page = Page(url, html)
        self.visited[url] = page
        for link in page.links:
            if not self.is_excluded(link):
                self.queue.append(link)

        return True

    def get_response(self, url, context):
        try:
            response = request.urlopen(url, context=context)
            html = response.read().decode('utf8')
            return html
        except HTTPError:
            return None
        except UnicodeDecodeError:
            return None
        except:
            time.sleep(10)
            return None

    def set_parents(self):
        for url in self.visited:
            page = self.visited[url]
            for child in page.links:
                if child in self.visited:
                    child_page = self.visited[child]
                    child_page.parents.add(url)

    def is_excluded(self, link):
        for path in self.exclusions:
            if path in link:
                return True
        return False

    def serialize(self):
        # Write to the stream
        out_s = open('data/pages_new_test.p', 'wb')
        pickle.dump(self.visited, out_s)
        pickle.dump(self, open('data/crawler_new_test.p', 'wb'))
        # pickle.dumps(self.visited, open('data/pages.p', 'wb'))


if __name__== "__main__":
    sys.path.append("search/engine/")
    # crawler = WebCrawler("https://www.depaul.edu/")
    crawler = pickle.load(open('data/crawler_new_test.p', 'rb'))
    pickle.dump(crawler, open('data/crawler_new_test', 'wb'))
    # crawler.crawl(6000)
    # crawler.serialize()
    # index = InvertedIndex(crawler.visited)
    # index.serialize()


