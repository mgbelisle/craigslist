craigslist
==========

Craigslist crawler

```
$ ./main.py --help
usage: main.py [-h] [--query QUERY [QUERY ...]]
               [--category CATEGORY [CATEGORY ...]] [--days DAYS]
               [--locales LOCALES] [--out OUT]

Crawls through craigslist looking for specified queries, then writes the
results to a file

optional arguments:
  -h, --help            show this help message and exit
  --query QUERY [QUERY ...]
                        Search term to query (default is ['toyota'])
  --category CATEGORY [CATEGORY ...]
                        Category to search for (default is ['cta'])
  --days DAYS           Number of past days to search (default is 2)
  --locales LOCALES     Locales file to search (default is close_locales.json)
  --out OUT             File to write output (default is results.json)
```
