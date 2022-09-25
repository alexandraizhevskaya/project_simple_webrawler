import argparse
from crawler import run_crawling
import logging
logging.basicConfig(level=logging.INFO)


def main():

    # add parser
    parser = argparse.ArgumentParser(description='Process url link to get its content '
                                                 'and the content of the linked pages')
    parser.add_argument('-url', required=True, help='Link to start crawling with', type=str)
    parser.add_argument('-walk-depth', required=True,  help='Depth of recursive crawling',
                        type=int)

    # parse the arguments
    args = parser.parse_args()
    url = args.url
    walk_depth = args.walk_depth

    # run main func
    if walk_depth > 10:
        logging.warning('Walk depth is big, hence, recursive crawling can take long time or go wrong due to blocking.')
    logging.info(f'Start crawling  url: {url}. The depth of crawling: {walk_depth}')
    run_crawling(url, walk_depth)


if __name__ == '__main__':
    main()

