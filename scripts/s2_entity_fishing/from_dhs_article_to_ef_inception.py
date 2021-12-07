

# %%
from csv import DictReader
import json
from os import path
from random import randint, seed

import requests as r

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from dhs_scraper import DhsArticle
from inception_fishing import *
from file_paths import S2_ENTITY_FISHING_ANNOTATION_OUTPUT_FILE, S2_ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER, S2_INCEPTION_IMPORT_FOLDER, S2_CLEF_HIPE_PRED_FILE, S1_WIKIDATA_DHS_WIKIPEDIA_LINKS, localize

from s0_sample_dhs_training_data_for_entity_fishing import sampled_articles_by_language, sampled_languages

# %%

language = "fr"

sampled_articles = sampled_articles_by_language[language]



# %% dhs_wikidata_wikipedia_links_dict

with open(S1_WIKIDATA_DHS_WIKIPEDIA_LINKS) as csvfile:
    dhs_wikidata_wikipedia_links_list = [r for r in DictReader(csvfile, delimiter=",")]
dhs_wikidata_wikipedia_links_dict=dict()
if dhs_wikidata_wikipedia_links_list is not None: 
    dhs_wikidata_wikipedia_links_dict = {
        l["dhsid"]: l
        for l in dhs_wikidata_wikipedia_links_list
    }

# %%
#dhs_article = sampled_articles[0]
#document = Document.from_dhs_article(dhs_article, dhs_wikidata_wikipedia_links_dict)
# %%

sampled_documents_and_articles_by_lng = {
    lng: [
        (
            Document.from_dhs_article(dhs_article, dhs_wikidata_wikipedia_links_dict, wikipedia_page_name_language=lng),
            dhs_article
        )
        for dhs_article in articles
    ]
    for lng, articles in sampled_articles_by_language.items()
}
# %%

def replace_dhs_article_initial_in_document(document:Document, dhs_article:DhsArticle):
    if dhs_article.initial is not None:
        return document.replace_regex(dhs_article.initial+r"\.", dhs_article.title)
    else:
        return []


# %%

sampled_articles_initials_replacements_by_language = {lng:dict() for lng in sampled_languages}
for lng, documents_and_articles in sampled_documents_and_articles_by_lng.items():
    print(f"\n\nSampling articles for language {lng}\n=========================================")
    for d,a in documents_and_articles:
        initials_replacements = replace_dhs_article_initial_in_document(d, a)
        sampled_articles_initials_replacements_by_language[lng][a.id] = initials_replacements
        with open(path.join(localize(S2_ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER, lng),d.name+f".{lng}.txt"), "w") as rawtext_file:
            print(f"writing for article {d.name}")
            rawtext_file.write(d.text)
# %%
