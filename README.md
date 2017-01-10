# kanmusu-tone
How do they say?

## Dependency
- [scrapy](https://scrapy.org/)

## Quick Start
1. Crawl [kcwiki](https://zh.kcwiki.moe) for information.
  ```
  cd crawler
  scrapy crawl kcwiki-zh -o ../data/kanmusu.jsonlines
  ```

2. Process for the statistics.
  ```
  python stat_*.py data/kanmusu.jsonlines data/kanmusu.csv
  ```

3. Check `.csv` for results.
