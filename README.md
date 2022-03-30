# Leetcode parser

Parses code tasks from leetcode.com website and writes them in a .csv file

## Installation

1) Clone repo:

`$ git clone <repo address>`

and cd into directory

2) <i>optionally</i> - initialize and start virtual environment with:

`$ python3 -m venv env`
`$ source env/bin/activate`

3) Install dependencies:

`$ pip install -r requirements.txt`

## Usage

`$ python3 -m lc_parcer [-t, --test] [-d, --debug] [-l, --log] [-p, pages]`

#### Arguments:
-t, --test:   run tests
-d, --debug:  set logging to debug (default logging level - info)
-l, --log:    write logs into file. Usage: <i>-l mylogs.log</i>. If not set, logs would go to stdout.
-p, --pages:  set max pages to parse from leetcode tasks. Usage: <i>-p 8</i>. By default, script downloads only first page.