import click
from crawler.crawler import Crawler
from dotenv import load_dotenv
import os
load_dotenv()

# environment variables
URL = os.environ.get("URL")
MAX_URL = os.environ.get("MAX_URL")

@click.command()
@click.option('--start_point', default=URL, help='Starting point URL for the crawler.', type=str)
@click.option('--max_url', default=MAX_URL, help='Number of URLs to crawl.', type=int)
def run_crawler(start_point, max_url):
    crawler = Crawler(urls=[str(start_point)], max_url=max_url)
    crawler.run()
    stats = crawler.get_crawler_statistics()
    print()
    print(stats)

if __name__ == '__main__':
    run_crawler()
