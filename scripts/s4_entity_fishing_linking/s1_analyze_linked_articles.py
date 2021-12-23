# %%


import sys

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle, stream_to_jsonl

from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S4_JSONL_ALL_ARTICLES_LINKED_FILE, localize
# %%
"""
"""



# %%


def get_dhsid(text_link):
    return text_link.get("dhsid")
def get_wikidata_url(text_link):
    annotation = text_link.get("annotation")
    if annotation is not None:
        return annotation.get("wikidata_entity_url")
def get_wikipedia_url(text_link):
    annotation = text_link.get("annotation")
    if annotation is not None:
        return annotation.get("wikidata_entity_url")

def 


# %%

lng="fr"
max_nb_articles=10


jsonl_linked_articles_file = localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE, lng)

articles_ids_titles = list()
linked_articles = list(DhsArticle.load_articles_from_jsonl(
    localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE,lng),
    indices_to_keep=[i for i in range(max_nb_articles)]
))



# %%
