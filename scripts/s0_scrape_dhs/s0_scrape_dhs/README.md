
# Scrape the whole DHS content

- `scrape.py`: code to scrape the whole DHS
- `dhs_stats.py`: code for descriptive stats on the DHS corpus



# Descriptive stats on the DHS corpus

todo stats:
- most frequent categories of articles
- distribution of length of articles in character
    - and by category
- entities linked to wikidata by category

other stats:
- number of sources
- external databases (GND, documents diplomatiques suisses)
- time-distribution of revisions

# Other

Note on the scrapes downloaded arounde 5.10.2021:
- links in the "En bref" section of articles have been scraped as tags (in addition to bref), solution: remove tags with url starting with "/article"