# started with file script s0_scrape_dhs/s0_scrape_dhs/s2_dhs_stats.py as basis

# %%
from os import path
from random import sample, seed

import json
from langcodes import tag_match_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from inception_fishing import * 
from data_file_paths import *
from plot_styles import *

# %%

language = "fr"

polities_dtf = pd.read_csv(s2_polities_list_csv)
# restore hds id to their proper str format
polities_dtf.hds_article_id = polities_dtf.hds_article_id.apply(lambda id: str(id))
polities_dtf.hds_article_id = polities_dtf.hds_article_id.apply(lambda id: ((6-len(id))*"0")+id)
polities_dtf.loc[polities_dtf.typology.isna(),"typology"] = None
polities_dtf.loc[polities_dtf.geoidentifier.isna(), "geoidentifier"] = None

polities_dtf[50:70]
# %%

polities_dtf[polities_dtf.typology.apply(lambda x: x is not None)].head(20)
# %%

articles_jsonl_file = localize(S0_JSONL_ALL_ARTICLES_PARSED_FILE, language)
articles = list(DhsArticle.load_articles_from_jsonl(
    articles_jsonl_file,
    ids_to_keep=set(polities_dtf.hds_article_id)
))
articles_dict = {a.id: a for a in articles}

# %%

polities_dtf["article"] = polities_dtf.hds_article_id.apply(lambda id: articles_dict[id])
polities_dtf.head()


# %%

# Create documents from articles, replacing article initials with proper toponym

def create_document(polities_dtf_row):
    """Creates document from article + toponym"""
    a = polities_dtf_row[1]["article"]
    toponym = polities_dtf_row[1]["toponym"]
    d = dhs_article.document_from_dhs_article(a, include_title_annotations=False, replace_initial_from_dhs_article=False)
    d.extra_fields["initial_replacement"] = dhs_article.document_replace_initial_from_dhs_article(d, a, replacement=toponym)
    return d

polities_dtf["document"] = [
    create_document(row)
    for row in polities_dtf.iterrows()
]
    

# %%

# Writing articles txt files to be annotated in inception

seed(54367)

sampled_articles_ids = [a.id for a in sample(articles, 100)]
with open(s2_sampled_polities_for_annotation_json, "w") as f:
    json.dump(sampled_articles_ids, f, ensure_ascii=False)

for i,row in polities_dtf.iterrows():
    if row["hds_article_id"] in sampled_articles_ids:
        polity_txt_path = path.join(s2_polities_txt_folder, row["hds_article_id"]+"_"+row["article_title"].replace('/','_')+".txt")
        with open(polity_txt_path, "w") as f:
            f.write(row["document"].text)
# %%
