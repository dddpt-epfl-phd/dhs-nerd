# %%

import json
from os import path
import sys

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import dhs_article
from dhs_scraper import DhsArticle, stream_to_jsonl

from data_file_paths import S4_JSONL_ALL_ARTICLES_LINKED_FILE, S5_WEBSITE_SINGLE_ARTICLES_LOCALIZED_FOLDER, localize
# %%
"""
This scripts load all the DhsArticles in S0_JSONL_ALL_ARTICLES_FILE and writes them to single json files
"""
max_nb_articles=40000


# LOAD LINKED ARTICLES AND STREAMING THEM TO INDIVIDUAL JSON
default_language="it"
entity_fishing_timeout = None

language = default_language
possible_languages = ["fr", "de", "it"]
if len(sys.argv)>1:
    if sys.argv[1] in possible_languages:
        language = sys.argv[1]
    else:
        raise Exception(f"s0_scrape.py: unrecognized language argument from sys.argv[1]: '{sys.argv[1]}'. Must be one of {possible_languages}")




jsonl_linked_articles_file = localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE, language)
json_folder = localize(S5_WEBSITE_SINGLE_ARTICLES_LOCALIZED_FOLDER, language)

articles_ids_titles = list()
for i,a in enumerate(DhsArticle.load_articles_from_jsonl(
            localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE,language),
            indices_to_keep=[i for i in range(max_nb_articles)]
        )):
    with open(path.join(json_folder, f'{a.id}.json'), 'w') as f:
        print(f"{i} writing {language} json for {a.title}")
        json.dump(a.to_json(as_dict=True), f)
    articles_ids_titles.append((a.id, a.search_result_name))

index_json = localize(S5_WEBSITE_SINGLE_ARTICLES_LOCALIZED_FOLDER, "indices/"+language+".json")
with open(index_json, 'w') as f:
    print(f"writing index json for {language}")
    json.dump(articles_ids_titles, f)


# %%

# %%
