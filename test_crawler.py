import unittest
from crawler_class import SimpleCrawler


# test on habr
class MyTestCase(unittest.TestCase):

    def check_uniqueness(self):
        url = 'https://habr.com/ru/all/'
        crawler = SimpleCrawler()
        crawler.crawl(url=url,
                      walk_depth=1,
                      file_name='urls.txt')
        with open('urls.txt', 'r') as f:
            crawled_sites = [url_link.strip('\n').split() for url_link in f.readlines()]
        self.assertTrue(len(crawled_sites) == len(set(crawled_sites)))

    def check_consistency(self):
        url = 'https://habr.com/ru/all/'
        crawler = SimpleCrawler()
        crawler.crawl(url=url,
                      walk_depth=1,
                      file_name='urls1.txt')
        crawler.reboot()
        crawler.crawl(url=url,
                      walk_depth=1,
                      file_name='urls2.txt')

        with open('urls1.txt', 'r') as f:
            crawled_sites1 = [url_link.strip('\n').split() for url_link in f.readlines()]
        with open('urls2.txt', 'r') as f:
            crawled_sites2 = [url_link.strip('\n').split() for url_link in f.readlines()]
        self.assertEqual(crawled_sites1, crawled_sites2)

    def test_inclusion(self):
        url = 'https://habr.com/ru/all/'
        crawler = SimpleCrawler()
        crawler.crawl(url=url,
                      walk_depth=1,
                      file_name='urls1.txt')
        crawler.reboot()
        crawler.crawl(url=url,
                      walk_depth=2,
                      file_name='urls2.txt')

        with open('urls1.txt', 'r') as f:
            crawled_sites1 = [url_link.strip('\n').split()[1] for url_link in f.readlines()]
        with open('urls2.txt', 'r') as f:
            crawled_sites2 = [url_link.strip('\n').split()[1] for url_link in f.readlines()]
        for url in crawled_sites1:
            self.assertIn(url, crawled_sites2)


if __name__ == '__main__':
    unittest.main()
