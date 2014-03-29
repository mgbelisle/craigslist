#!/usr/bin/env python3

"""
Generates a list of locales available on craigslist
"""

import re
import json

from bs4 import BeautifulSoup
import requests


URL = 'http://geo.craigslist.org/iso/us'
LOCALE_RE = re.compile(r'^http://(?P<locale>[a-z]+)\.craigslist\.org/$')

if __name__ == '__main__':
    # Gets all the locales
    response = requests.get(URL)
    soup = BeautifulSoup(response.text)
    links = soup.findAll('a', href=LOCALE_RE)
    locales = [LOCALE_RE.match(l['href']).group('locale')
               for l in links]

    # Saves the list
    print(json.dumps(locales, indent=4))
