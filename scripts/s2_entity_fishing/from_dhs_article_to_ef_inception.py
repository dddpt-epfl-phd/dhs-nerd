

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
from utils import spacy_models_by_lng
from file_paths import S2_ENTITY_FISHING_ANNOTATION_OUTPUT_FILE, S2_ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER, S2_INCEPTION_IMPORT_FOLDER, S2_CLEF_HIPE_PRED_FILE, S1_WIKIDATA_DHS_WIKIPEDIA_LINKS, localize

from s0_sample_dhs_training_data_for_entity_fishing import sampled_articles_by_language

# %%

language = "fr"

sampled_articles = sampled_articles_by_language[language]


with open(S1_WIKIDATA_DHS_WIKIPEDIA_LINKS) as csvfile:
    dhs_wikidata_wikipedia_links_list = [r for r in DictReader(csvfile, delimiter=",")]


dhs_article = sampled_articles[0]
text_blocks_separator = "\n"
#Document.from_dhs_article(sampled_articles[0], dhs_wikidata_wikipedia_links)
######################################

# %%

text_blocks = dhs_article.parse_text_blocks()
whole_text = ""
annotations = []
for tag, text in text_blocks:
    new_whole_text = whole_text+text
    annotations.append(Annotation(
        len(whole_text),
        len(new_whole_text),
        extra_fields = {"type": "text_block", "dhs_html_tag": tag}
    ))
    whole_text = new_whole_text+text_blocks_separator


# %%

# adding text_links

dhs_wikidata_wikipedia_links_dict=dict()
if dhs_wikidata_wikipedia_links_list is not None: 
    dhs_wikidata_wikipedia_links_dict = {
        l["dhsid"]: l
        for l in dhs_wikidata_wikipedia_links_list
    }

# %%
# '/fr/articles/008248/2015-02-04/'
dhs_article_id_from_url_regex = re.compile(r"(fr|de|it)/articles/(\d+)/")

text_links_per_blocks = dhs_article.parse_text_links()
for i, text_links in enumerate(text_links_per_blocks):
#if True:
    #i = 3
    #text_links = text_links_per_blocks[i]
    ####### 
    text_block_start = annotations[i].start
    for text_link in text_links:
    #if True:
        #text_link = text_links[0]
        #####
        start, end, mention, href = text_link.values()
        # get text link correspondance in wikidata & wikipedia (if present)
        wikidata_entity_url = None
        wikipedia_page_title = None
        dhs_id_match = dhs_article_id_from_url_regex.search(href)
        if dhs_id_match:
            dhs_id = dhs_id_match.group(2)
            wikidata_entry = dhs_wikidata_wikipedia_links_dict.get(dhs_id)
            if wikidata_entry:
                wikidata_entity_url = wikidata_entry["item"]
                wikidata_entity_url = wikidata_entity_url if wikidata_entity_url!="" else None
                wikipedia_page_title = wikidata_entry["name"+language]
                wikipedia_page_title = wikipedia_page_title if wikipedia_page_title!="" else None
        annotations.append(Annotation(
            text_block_start+start,
            text_block_start+end,
            wikidata_entity_url = wikidata_entity_url,
            wikipedia_page_title = wikipedia_page_title,
            mention = mention,
            extra_fields={"type": "text_link", "dhs_href": href}
        ))

# %%

document = Document(dhs_article.title, annotations, whole_text)