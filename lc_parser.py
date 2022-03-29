import re
import sys
import csv
import logging
import subprocess
from optparse import OptionParser

import requests
from bs4 import BeautifulSoup


PAGE_LINK = 'https://leetcode.com/problemset/algorithms/'
FIELD_NAMES = ['id', 'title', 'acceptance', 'difficulty']
DEFAULT_FILENAME = 'tasks.csv'


def make_list(table: BeautifulSoup) -> list:
    result = []
    for row in table.contents:
        r = []
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
        result.append(r)
    return result


def main():
    r = requests.get(PAGE_LINK)
    logging.info('Downloaded page. Status code: %s' % r.status_code)
    soup = BeautifulSoup(r.text, features='html.parser')
    table = soup.find(role='rowgroup')
    rows = make_list(table)
    with open(DEFAULT_FILENAME, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(FIELD_NAMES)
        writer.writerows(rows)
    logging.info('Written file %s' % file.name)


def runtest():
    command = ['python', '-m', 'unittest', '-v']
    subprocess.run(command)


if __name__ == '__main__':
    op = OptionParser()
    op.add_option("-t", "--test", action="store_true", default=False)
    op.add_option("-l", "--log", action="store", default=None)
    op.add_option("--debug", action="store_true", default=False)
    opts, args = op.parse_args()
    logging.basicConfig(filename=opts.log,
                        level=(
                            logging.INFO if not opts.debug else logging.INFO),
                        format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S')
    if opts.test:
        runtest()
        sys.exit(0)
    logging.info('Leetcode parser started with options: %s' % opts)
    try:
        main()
    except Exception as e:
        logging.exception("Unexpected error: %s" % e)
        sys.exit(1)
