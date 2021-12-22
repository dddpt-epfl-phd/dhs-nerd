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

# LINKING AND STREAMING LINKED ARTICLES TO JSONL
lng="de"
max_nb_articles=2500


jsonl_linked_articles_file = localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE, lng)
json_folder = localize(S5_WEBSITE_SINGLE_ARTICLES_LOCALIZED_FOLDER, lng)

articles_ids_titles = list()
for a in DhsArticle.load_articles_from_jsonl(
            localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE,lng),
            indices_to_keep=[i for i in range(max_nb_articles)]
        ):
    with open(path.join(json_folder, f'{a.id}.json'), 'w') as f:
        print(f"writing json for {a.title}")
        json.dump(a.to_json(as_dict=True), f)
    articles_ids_titles.append((a.id, a.title))

index_json = localize(S5_WEBSITE_SINGLE_ARTICLES_LOCALIZED_FOLDER, "indices/"+lng+".json")
with open(index_json, 'w') as f:
    print(f"writing index json for {lng}")
    json.dump(articles_ids_titles, f)


# %%

# %%
