import os
import shutil
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO)


def run_crawling(url: str,
                 walk_depth: int = 2,
                 file_name: str = 'urls.txt',
                 data_dir: str = 'data'
                 ) -> None:

    # idx to write indices correctly
    idx = 1
    # visited set to depth-search correctly
    visited = set()

    def crawl(url: str,
              walk_depth: int = 2,
              file_name: str = 'urls.txt',
              data_dir: str = 'data',
              ) -> None:

        nonlocal idx, visited

        # add random headers to make requests less suspicious
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

        # try to get url, processing exceptions
        try:
            req = requests.get(url, headers=headers, timeout=5)
            if req.status_code != 200:
                logging.error(f'Request status code for id {idx} is not 200. Please, search '
                              f'the meaning of the following request status: {req.status_code}')
            html_page = req.text

        except requests.Timeout as e:
            logging.error('Probably, the site is blocking crawler:(')
            logging.error(str(e))
        except requests.RequestException as e:
            logging.error('Something went wrong with the request')
            logging.error(str(e))
        else:
            # if it is the first page being processed, rewrite existing txt file or make a new one
            if idx == 1:
                with open(file_name, 'w') as f:
                    f.write(f'{idx}.{url}' + '\n')

                # if there is no directory - create it. If there is directory with such name, remove it recursively
                if not os.path.exists(data_dir):
                    os.mkdir(data_dir)
                else:
                    shutil.rmtree(data_dir)
                    os.mkdir(data_dir)

            else:
                # append new lines to file without rewriting its content
                with open(file_name, 'a') as f:
                    f.write(f'{idx} {url}' + '\n')

            # save html file to directory
            with open(os.path.join(data_dir, f'{idx}.html'), 'w') as f:
                f.write(html_page)
            logging.info(f'Processing file: id {idx}; url {url}')

            # parse page and increment idx variable
            soup = BeautifulSoup(html_page, 'html.parser')
            idx += 1

            # get the links
            links_set = set()
            for next_link in soup.find_all('a'):
                new_url = next_link.get('href')

                # check whether they are valid and belong to the web site
                if new_url and new_url.startswith('/'):
                    new_url = urljoin(url, new_url)
                    # if new_url and new_url.startswith('http') and new_url not in visited:
                    links_set.update([new_url])

            # walk recursively till the given walk_depth is reached
            if walk_depth > 0:
                for i in links_set:
                    if i not in visited:
                        # mark url as visited
                        visited.update([i])
                        crawl(i, walk_depth - 1, file_name, data_dir)

    crawl(url=url, walk_depth=walk_depth, file_name=file_name, data_dir=data_dir)

# crawl('https://www.rbc.ru/')
# crawl('https://habr.com/ru/all/')
