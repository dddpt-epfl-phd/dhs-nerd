# %%


import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, stream_to_jsonl
from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S0_JSONL_ALL_ARTICLES_PARSED_FILE, localize

# %matplotlib inline

"""
Loads all the DhsArticle with their page_content from S0_JSONL_ALL_ARTICLES_FILE, parses them and save them back to S0_JSONL_ALL_ARTICLES_PARSED_FILE file.

Used mainly for statistics in s2_dhs_stats.py.
"""

language="fr"


jsonl_articles_content_file = localize(S0_JSONL_ALL_ARTICLES_FILE, language)
jsonl_articles_parsed_file = localize(S0_JSONL_ALL_ARTICLES_PARSED_FILE, language)

buffer_size = 10
info_interval = 100

# %%

def parsed_articles_without_page_content_generator(articles, already_visited_ids, info_interval=info_interval):
    for i, a in enumerate(articles):
        if a.id not in already_visited_ids:
            a.parse_article()
            if i % info_interval == 0:
                print(f"parsing articles, currently at {i}th article....")
            a.drop_page()
            yield a


# %%

unparsed_articles = list(DhsArticle.load_articles_from_jsonl(jsonl_articles_content_file))

# %%



already_visited_ids = set(DhsArticle.get_articles_ids(jsonl_articles_parsed_file))

# %%
stream_to_jsonl(
    jsonl_articles_parsed_file,
    parsed_articles_without_page_content_generator(
        unparsed_articles,
        already_visited_ids
    ),
    buffer_size=buffer_size
)
# %%
