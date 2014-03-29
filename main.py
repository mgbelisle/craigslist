#!/usr/bin/env python3

"""
Crawls through craigslist looking for specified queries, then writes the results to a file
"""

from argparse import ArgumentParser
from argparse import FileType
from datetime import datetime
from datetime import timedelta
import json
import logging
import os
import re

from bs4 import BeautifulSoup
import requests


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
HREF_RE = re.compile(r'/[a-z]+/\d+\.html')

DEFAULT_QUERIES = ['toyota']
DEFAULT_CATEGORIES = ['cto']
DEFAULT_DAYS = 2
DEFAULT_LOCALES = os.path.relpath(os.path.join(THIS_DIR, 'close_locales.json'))
DEFAULT_OUT = os.path.relpath(os.path.join(THIS_DIR, 'results.json'))

parser = ArgumentParser(description=__doc__)
parser.add_argument('--query',
                    nargs='+',
                    default=DEFAULT_QUERIES,
                    help='Search term to query (default is {})'.format(
                        DEFAULT_QUERIES))
parser.add_argument('--category',
                    nargs='+',
                    default=DEFAULT_CATEGORIES,
                    help='Category to search for (default is {})'.format(
                        DEFAULT_CATEGORIES))
parser.add_argument('--days',
                    type=int,
                    default=DEFAULT_DAYS,
                    help='Number of past days to search (default is {})'.format(
                        DEFAULT_DAYS))
parser.add_argument('--locales',
                    type=FileType('r'),
                    default=DEFAULT_LOCALES,
                    help='Locales file to search (default is {})'.format(
                        DEFAULT_LOCALES))
parser.add_argument('--out',
                    type=FileType('w'),
                    default=DEFAULT_OUT,
                    help='File to write output (default is {})'.format(
                        DEFAULT_OUT))
args = parser.parse_args()


def search(locale=None, category=None, query=None):
    """
    Returns search results as a list of dicts
    """
    response = requests.get('http://{}.craigslist.org/search/'.format(locale),
                            params={'query': query, 'catAbb': category})
    soup = BeautifulSoup(response.text)
    results = []
    for item_tag in soup.findAll('p'):
        date_tag = item_tag.find('span', class_='date')
        if not date_tag:
            logging.warning('Could not find date tag: {}'.format(item_tag))
            continue
        dt = datetime.strptime(date_tag.text, '%b %d').replace(
            year=datetime.now().year)
        if dt < datetime.now()- timedelta(days=args.days):
            continue
        try:
            price = item_tag.find('span', class_='price').text
        except AttributeError:
            price = None
        try:
            href = item_tag.find('a', href=HREF_RE)['href']
        except AttributeError:
            logging.warning('Could not find href: {}'.format(item_tag))
            continue
        if href.startswith('http://'):
            continue
        href = 'http://{}.craigslist.org'.format(locale) + href
        try:
            desc = item_tag.find_all('a', href=HREF_RE)[1].text
        except (AttributeError, IndexError):
            logging.warning('Could not find description tag: {}'.format(item_tag))
            desc = None
        results.append({
            'date': dt.isoformat(),
            'price': price,
            'desc': desc,
            'href': href,
        })
    print('{} matches on {}'.format(len(results), response.url))
    return results

if __name__ == '__main__':
    try:
        locales = json.load(args.locales)
    except ValueError:
        exit('Could not parse locales file')
    results = {
        '{}/{}/{}'.format(locale, category, query): search(locale=locale,
                                                           category=category,
                                                           query=query)
        for locale in locales
        for category in args.category
        for query in args.query
    }
    results = dict(i for i in results.items() if i[1])
    json.dump(results, args.out, indent=4)
