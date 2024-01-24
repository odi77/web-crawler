import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
import os
import requests
from time import sleep, time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from usp.tree import sitemap_tree_for_homepage
import validators
load_dotenv()




logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Utils:
    def __init__(self) -> None:
        pass

    def write_txt_file(self, path, document):
        file = open(path, 'w')
        for line in document:
            file.write(line + os.linesep)
        file.close()


class Crawler:

    def __init__(
        self,
        urls=[],
        max_url=os.environ.get("MAX_URL"),
        wait_time=5
    ):
        self.__visited_urls = []
        self.__visited_sitemaps = []
        self.__crawled_urls = []
        self.__urls_to_visit = urls
        self.__MAX_URL = int(max_url)
        if wait_time < 5:
            wait_time = 5
        self.wait_time = wait_time
        self.homepage_fail = 0
        self.sitemap_fail = 0
        self.crawl_fail = 0

    def get_visited_urls(self):
        '''
        Returns the list of all the links that have been visited
        '''
        return self.__visited_urls

    def get_crawled_urls(self):
        '''
        Returns the list of all the urls that can be crawled
        '''
        return self.__crawled_urls

    def get_urls_to_visit(self):
        '''
        Returns the temporary list of all links found on a given page
        '''
        return self.__urls_to_visit

    def get_visited_sitemaps(self):
        '''
        Returns the list of all sitemaps that have been visited
        '''
        return self.__visited_sitemaps

    def get_html_from_url(self, url):
        '''
        Gets the text of the web page for a given URL
        '''
        try:
            return requests.get(url).text
        except Exception:
            logging.exception(f'URL {url} not found')
            self.homepage_fail += 1

    def get_linked_urls(self, url, html):
        '''
        Find all the links in a HTML page
        '''
        soup = BeautifulSoup(html, 'html.parser')
        links = list()
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('http'):
                path = urljoin(url, path)
                links.append(path)
        return links

    def add_crawled_urls(self, url):
        '''
        Add a link to the list of crawled URLs if not already in it.
        '''
        if url not in self.__crawled_urls:
            self.__crawled_urls.append(url)

    def add_url_to_visit(self, url):
        if url not in self.__visited_urls and url not in self.__urls_to_visit:
            self.__urls_to_visit.append(url)

    def get_sitemap_from_url(self, url):
        homepage = self.get_homepage_url(url)
        if homepage not in self.__visited_sitemaps:
            sitemap_tree = sitemap_tree_for_homepage(homepage_url=homepage)
            for page in sitemap_tree.all_pages():
                self.add_url_to_visit(page.url)
            self.__visited_sitemaps.append(homepage)

    @staticmethod
    def is_crawlable(url):
        '''
        Check if a url can be crawled or not

        Returns
        -------
        bool : True if the url can be crawled, False if not.
        '''
        rp = RobotFileParser()
        scheme = urlparse(url).scheme
        domain = urlparse(url).netloc
        link = scheme + "://" + domain + "/robots.txt"
        rp.set_url(link)
        rp.read()
        return rp.can_fetch("*", url)

    @staticmethod
    def get_homepage_url(url):
        '''
        Get the homepage url from an url

        Example
        -------
        >>> url = "https://ensai.fr/double-diplome-universite-rome-sapienza/"
        >>> crawler = Crawler()
        >>> homepage = crawler.get_homepage(url)
        >>> print(homepage)
        "https://ensai.fr/"
        '''
        scheme = urlparse(url).scheme
        domain = urlparse(url).netloc
        homepage_url = scheme + "://" + domain + "/"
        return homepage_url

    @staticmethod
    def is_valid_url(url):
        '''
        Check if the url is valid
        '''
        return validators.url(str(url))

    def crawl(self, url, wait_time):
        '''
        Add links that are valid to the crawlable list and linked URLS to __urls_to_visit list
        + rule of politeness
        '''
        # add to crawled URLs if it is a valid URL
        is_valid = self.is_valid_url(url)
        if is_valid:
            # add to crawlable URLs
            self.add_crawled_urls(url=url)

            # politeness: waiting before crawling next url
            logging.info(f'Waiting {wait_time} seconds')
            sleep(wait_time)
        else:
            logging.warning(f'Invalid URL for {url}')

        # add links found in page to URLs to visit
        html = self.get_html_from_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        '''
        Performs the crawling. First it checks if there is any sitemap.
        Then it fetches all the possible URLs found in the document.
        Finally, every crawlable URLs is saved in a list then output in a txt file.
        '''
        start_time = time()
        while self.__urls_to_visit and len(self.__crawled_urls) < self.__MAX_URL:
            url = self.__urls_to_visit.pop(0)

            # use sitemap to crawl
            try:
                self.get_sitemap_from_url(url)
            except Exception:
                logging.exception(f'Failed to crawl {url} from sitemap')
                self.sitemap_fail += 1

            logging.info(f'Crawling {url}')
            try:
                is_crawlable = self.is_crawlable(url)
                if is_crawlable:
                    self.crawl(url, wait_time=self.wait_time)
                else:
                    logging.warning(f'URL {url} could not be crawled')
                    self.crawl_fail += 1
            except Exception:
                logging.exception(f'Failed to crawl {url}')
            finally:
                self.__visited_urls.append(url)

        # write crawled URLs in txt file
        toolbox = Utils()
        toolbox.write_txt_file(path='./crawled_webpages.txt', document=self.__crawled_urls)
        
        self.__execution_time = time() - start_time

    def get_crawler_statistics(self) -> str:
        '''
        Returns a string containing information about the crawling.
        '''
        return (
            f"--- Statistics ---\n"
            f"Took {round(self.__execution_time, 2)} seconds (approx. {round(self.__execution_time/60)} minutes)\n"
            f"{len(self.__urls_to_visit) + len(self.__visited_urls)} links found\n"
            f"{len(self.__visited_urls)} links visited\n"
            f"{len(self.__crawled_urls)} links crawled\n"
            f"{self.homepage_fail} homepage failed\n"
            f"{self.sitemap_fail} sitemap failed\n"
            f"{self.crawl_fail} crawl failed"
            )
