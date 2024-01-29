# ThreadCraft : A Multithreaded Web Crawler".

**ThreadCraft** is a web crawler app designed as part of Web mining class projects.
The project involves creating a single-threaded web crawler. The crawler starts from a specified URL (https://ensai.fr/) and downloads web pages, waiting at least five seconds before proceeding to the next page. It explores additional pages by analyzing link tags in previously visited documents, stopping exploration after encountering 5 links per page or reaching a total of 50 URLs. The program concludes by writing all discovered URLs to a file named crawled_webpages.txt

## Class Diagram

```mermaid
classDiagram
  class Utils {
    + write_txt_file(path: str, document: list): void
  }

  class Crawler {
    - __visited_urls: list
    - __visited_sitemaps: list
    - __crawled_urls: list
    - __urls_to_visit: list
    - __MAX_URL: int
    - wait_time: int
    - homepage_fail: int
    - sitemap_fail: int
    - crawl_fail: int

    + __init__(urls: list, max_url: int, wait_time: int)
    + get_visited_urls(): list
    + get_crawled_urls(): list
    + get_urls_to_visit(): list
    + get_visited_sitemaps(): list
    + get_html_from_url(url: str): str
    + get_linked_urls(url: str, html: str): list
    + add_crawled_urls(url: str): void
    + add_url_to_visit(url: str): void
    + get_sitemap_from_url(url: str): void
    + is_crawlable(url: str): bool
    + get_homepage_url(url: str): str
    + is_valid_url(url: str): bool
    + crawl(url: str, wait_time: int): void
    + run(): void
    + get_crawler_statistics(): str
  }



### Author

- [Cyrille NEBANGA](https://github.com/odi77)


## Quick start

First, you will need to clone the repository.
```bash
git clone https://github.com/odi77/web-crawler.git
cd web-crawler
```

Then, we will set a virtual environment and download the necessary packages.
```python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Before launching the crawler, you should create an `.env` file containing the default values:
```
URL = https://ensai.fr/
MAX_URL = 50
```

Finally, to launch the crawler there are several options:
```python
# to get some help
python3 main.py --help
# with default parameters
python3 main.py
# with specified parameters
python3 main.py --start_point "https://www.ensae.fr/" --max_url 100