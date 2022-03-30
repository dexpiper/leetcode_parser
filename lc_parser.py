import re
import sys
import csv
import logging
import subprocess
from optparse import OptionParser

import requests
from bs4 import BeautifulSoup
import progressbar


PAGE_LINK = 'https://leetcode.com/problemset/algorithms/'
FIELD_NAMES = ['id', 'title', 'acceptance', 'difficulty']
DEFAULT_FILENAME = 'tasks.csv'


def make_list(table: BeautifulSoup) -> tuple[list, int]:
    """
    Parse bs4-extracted HTML table and return:
    * rows as list of lists: [['cell', 'cell'], ['cell', 'cell'], ...]
    * errors as int
    """
    errors = 0
    result = []
    for row in table.contents:
        r = []
        try:
            for cell in row.contents:
                if not cell.text:
                    continue
                elif re.match(r'\d+\. \w', cell.text):
                    id, title = cell.text.split('. ')
                    r.append(int(id))
                    r.append(title)
                elif re.match(r'\d+\.\d%', cell.text):
                    r.append(float(cell.text[:-1]))
                else:
                    r.append(cell.text.lower())
        except Exception as exc:
            logging.error(
                'Cannot parse cell "%s" properly: %s' % (cell.text, exc))
            errors += 1
            r.append(cell.text)
        result.append(r)
    return result, errors


def parse_page(link: str, page_no: int = 1) -> tuple[list, int]:
    """
    Request html as str from <link>, find table and pass it to
    the table parser <make_list()>
    """
    r = requests.get(link, params={'page': page_no}, allow_redirects=True)
    logging.info(
        'Downloaded page %s. Status code: %s' % (r.url, r.status_code))
    soup = BeautifulSoup(r.text, features='html.parser')
    table = soup.find(role='rowgroup')
    if not len(table):
        logging.exception('Cannot parse table from %s' % r.url)
    rows, errors = make_list(table)
    return rows, errors


def main(base_page_link: str, max_pages: int = 1):
    results = []
    total_errors = 0
    for page_no in progressbar.progressbar(range(1, max_pages + 1)):
        rows, errors = parse_page(base_page_link, page_no=page_no)
        results.append((rows, errors))
        logging.debug(
            'Parsed %s rows from page No %s. Errors: %s' % (
                len(rows), page_no, errors)
        )
    total_errors = sum([r[1] for r in results])
    logging.info(
        'Parsed %s pages. Total errors: %s' % (max_pages, total_errors))
    with open(DEFAULT_FILENAME, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(FIELD_NAMES)
        for r in results:
            rows = r[0]
            writer.writerows(rows)
    logging.info('Written file %s' % file.name)


def runtest():
    command = ['python', '-m', 'unittest', '-v']
    subprocess.run(command)


if __name__ == '__main__':
    op = OptionParser()
    op.add_option("-t", "--test", action="store_true", default=False)
    op.add_option("-d", "--debug", action="store_true", default=False)
    op.add_option("-l", "--log", action="store", default=None)
    op.add_option("-p", "--pages", action="store", default=1)
    opts, args = op.parse_args()
    progressbar.streams.wrap_stderr()  # for progressbar correct work
    logging.basicConfig(filename=opts.log,
                        level=(
                            logging.INFO if not opts.debug else logging.DEBUG
                        ),
                        format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S')
    if opts.test:
        runtest()
        sys.exit(0)
    logging.info('Leetcode parser started with options: %s' % opts)
    try:
        main(base_page_link=PAGE_LINK, max_pages=int(opts.pages))
    except Exception as e:
        logging.exception('Unexpected error: %s' % e)
        sys.exit(1)
