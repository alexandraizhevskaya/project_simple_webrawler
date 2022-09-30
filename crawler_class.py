import os
import shutil
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import logging
from typing import Union, Set
logging.basicConfig(level=logging.INFO)


class SimpleCrawler:

    def __init__(self) -> None:
        """
        Class to process url link and links connected to it to the given depth.

        -idx - variable to assign indices to links being processed. It is incremented iteratively
        -visited - set with links that have already been visited to maintain consistency
        """
        self.idx = 1
        self.visited = set()
        # some random headers - it doesn't really help but why not
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    def get_html_page(self, url: str) -> Union[None, str]:
        """
        Get html content of a page with requests.
        If something goes wrong, returns None
        :param url: link to get html
        :return: html page or None
        """

        # try to get url, processing exceptions
        try:
            req = requests.get(url, headers=self.headers, allow_redirects=False, timeout=5)
            if req.status_code != 200:
                logging.error(f'Request status code for id {self.idx} is not 200. Please, search '
                              f'the meaning of the following request status: {req.status_code}')
            html_page = req.text
        # exception processing
        except requests.Timeout as e:
            logging.error('Probably, the site is blocking crawler:(')
            logging.error(str(e))
            html_page = None
        except requests.RequestException as e:
            logging.error('Something went wrong with the request')
            logging.error(str(e))
            html_page = None
        return html_page

    @staticmethod
    def get_all_links(html_page: str, url: str) -> Set:
        """
        Process raw html with bs and get all the links from the processed url (only nested counts)
        :param html_page: raw html content to process with beautiful soup
        :param url: link that is being processed
        :return: set of extracted links
        """
        # get the links
        soup = BeautifulSoup(html_page, 'html.parser')
        links_set = set()
        for next_link in soup.find_all('a'):
            new_url = next_link.get('href')

            # check whether they are valid and belong to the website
            if new_url and new_url.startswith('/'):
                new_url = urljoin(url, new_url)
                # if new_url and new_url.startswith('http') and new_url not in visited:
                links_set.update([new_url])
        return links_set

    @staticmethod
    def mkdir(data_dir: str) -> None:
        """
        utils function to make directory
        :param data_dir: directory name
        :return: None
        """
        # if there is no directory - create it. If there is directory with such name, remove it recursively
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        else:
            shutil.rmtree(data_dir)
            os.mkdir(data_dir)

    def write_txt(self, file_name: str, url: str, mode: str) -> None:
        """
        utils function to write lines to a text file
        :param file_name: name of txt file
        :param url: url that is being processed
        :param mode: mode of writing ('w', 'a')
        :return: None
        """
        with open(file_name, mode, encoding='utf-8') as f:
            f.write(f'{self.idx} {url}' + '\n')

    def write_file(self, data_dir: str, html_page: str) -> None:
        """
        utils function to write html file to a directory
        :param data_dir: name of directory to write file to
        :param html_page: html context of url
        :return: None
        """
        with open(os.path.join(data_dir, f'{self.idx}.html'), 'w', encoding='utf-8') as f:
            f.write(html_page)

    def crawl(self,
              url: str,
              walk_depth: int = 2,
              file_name: str = 'urls.txt',
              data_dir: str = 'data',
              ) -> None:
        """
        Main crawling function.
        It starts with a given url and processes all the linked urls recursively.
        As a result it saves a txt file with all the processed urls and the ids assigned to them
        and files with their html content
        :param url: link to start crawling
        :param walk_depth: depth of crawling
        :param file_name: name of file to write urls
        :param data_dir: name of directory to write texts
        :return: None
        """

        html_page = self.get_html_page(url)
        if html_page:
            # if it is the first page being processed, rewrite existing txt file or make a new one
            if self.idx == 1:
                self.write_txt(file_name, url, 'w')
                self.mkdir(data_dir)
            else:
                # append new lines to file without rewriting its content
                self.write_txt(file_name, url, 'a')
            # save html file to directory
            self.write_file(data_dir, html_page)

            logging.info(f'Processing file: id {self.idx}; url {url}')

            # parse page and increment idx variable
            self.idx += 1

            # get the links
            links_set = self.get_all_links(html_page, url)

            # walk recursively till the given walk_depth is reached
            if walk_depth > 0:
                for i in links_set:
                    if i not in self.visited:
                        # mark url as visited
                        print(walk_depth)
                        self.visited.update([i])
                        self.crawl(i, walk_depth - 1, file_name, data_dir)

    def reboot(self) -> None:
        """
        clean idx and visited set
        to crawl another url
        """
        self.idx = 1
        self.visited = set()
