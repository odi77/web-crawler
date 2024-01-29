# ThreadCraft : A Multithreaded Web Crawler".

**ThreadCraft** is a web crawler app designed as part of Web mining class projects.
The project involves creating a single-threaded web crawler. The crawler starts from a specified URL (https://ensai.fr/) and downloads web pages, waiting at least five seconds before proceeding to the next page. It explores additional pages by analyzing link tags in previously visited documents, stopping exploration after encountering 5 links per page or reaching a total of 50 URLs. The program concludes by writing all discovered URLs to a file named crawled_webpages.txt

```mermaid
graph TD;
  A[Start] -->|HTTP Request| B[Fetch URL];
  B -->|HTML Content| C[Extract Links];
  C -->|Valid URL| D[Add to Crawled URLs];
  D -->|Wait| E[Wait];
  E -->|HTTP Request| B;
  C -->|Invalid URL| F[Log Warning];
  F -->|Next URL| B;
  B -->|No URLs left| G[End];
  G -->|Crawled URLs| H[Write to File];
  H -->|Statistics| I[Get Crawler Statistics];
  I -->|End| J[End];
  ```

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