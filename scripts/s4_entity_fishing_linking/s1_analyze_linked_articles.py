# %%


from os import link
import sys

import pandas as pd

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle

from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S4_JSONL_ALL_ARTICLES_LINKED_FILE, localize
# %%
"""


Steps:
1) for each link get:
    - origin: original-dhs, entity-fishing
    - dhsid
    - wk page id
    - article
    - year of article
2) for each article get:
    - character count
    - year of version
    - nb of text_links
        - from original-dhs
        - from ef total
        - from ef to DHS
        - from ef to WK only
        - from ef to WD only
        - unlinked
"""



# %%


def get_dhsid(text_link):
    return text_link.get("dhsid")
def get_wikidata_url(text_link):
    annotation = text_link.get("annotation")
    if annotation is not None:
        return annotation.get("wikidata_entity_url")
def get_wikipedia_page_id(text_link):
    annotation = text_link.get("annotation")
    if annotation is not None:
        return annotation.get("wikipedia_page_id")

ORIGIN_FROM_ENTITY_FISHING = "entity_fishing"
ORIGIN_FROM_DHS = "original_dhs"
def get_origin(text_link):
    origin = text_link.get("origin")
    if origin is None:
        return ORIGIN_FROM_DHS
    return origin

# %%

lng="fr"
max_nb_articles=1000



linked_articles = list(DhsArticle.load_articles_from_jsonl(
    localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE,lng),
    indices_to_keep=[i for i in range(max_nb_articles)]
))


# %%


def article_text_links_stats(article: DhsArticle):
    nb_from_dhs = 0
    nb_from_ef = 0
    nb_to_dhs = 0
    nb_to_wk = 0
    nb_to_wd = 0
    nb_unlinked = 0
    for text_block in article.text_links:
        for tl in text_block:
            origin = get_origin(tl)
            if origin==ORIGIN_FROM_DHS:
                nb_from_dhs+=1
            elif origin==ORIGIN_FROM_ENTITY_FISHING:
                nb_from_ef+=1
                if get_dhsid(tl) is not None:
                    nb_to_dhs+=1
                elif get_wikipedia_page_id(tl) is not None:
                    nb_to_wk+=1
                elif get_wikidata_url(tl) is not None:
                    nb_to_wd+=1
                else:
                    nb_unlinked+=1
    return {
        "dhsid": article.id,
        "year": int(article.version[0:4]),
        "nb_char": len(article.text),
        "nb_from_dhs": nb_from_dhs,
        "nb_from_ef": nb_from_ef,
        "nb_to_dhs": nb_to_dhs,
        "nb_to_wk": nb_to_wk,
        "nb_to_wd": nb_to_wd,
        "nb_unlinked": nb_unlinked,
    }

# %%

links_stats_per_article = pd.DataFrame([article_text_links_stats(a) for a in linked_articles])
links_stats_per_article


# %%

links_stats_per_article.describe()

# %%

aarau = [a for a in linked_articles if a.id=="001620"][0]
#[tl.get("origin") for tb in aarau.text_links for tl in tb]

# %%
