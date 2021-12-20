# %%


import sys

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle, stream_to_jsonl

from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S4_JSONL_ALL_ARTICLES_LINKED_FILE, localize
# %%
"""
This scripts load all the DhsArticles in S0_JSONL_ALL_ARTICLES_FILE, links them with entity-fishing and streams them back into a json in S4_JSONL_ALL_ARTICLES_LINKED_FILE


Todo
1) DONE re-integration of doc.annotations in dhs_article.text_links
2) DONE test & ensure DhsA to jsonl works correctly with both text_content and text_links
3) DONE write code for whole of step 1) DhsA through EF
4) create mDhsA data-structure
5) write code for step 2) Unify DhsAs into mDhsAs
"""

lng="fr"


jsonl_linked_articles_file = localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE, lng)

linked_articles = list(DhsArticle.load_articles_from_jsonl(jsonl_linked_articles_file))


# %%
