#!/usr/bin/env python3

"""
Prints a list of the high level craigslist categories
"""

from bs4 import BeautifulSoup
import requests


URL = 'http://bozeman.craigslist.org/'

if __name__ == '__main__':
    response = requests.get(URL)
    soup = BeautifulSoup(response.text)
    options = soup.findAll('option')
    for option in options:
        print('{v}: {t}'.format(v=option['value'], t=option.text))
