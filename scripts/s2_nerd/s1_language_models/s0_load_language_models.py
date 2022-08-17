# started with file script s0_scrape_dhs/s0_scrape_dhs/s2_dhs_stats.py as basis

# %%
import json
from langcodes import tag_match_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from data_file_paths import *
from plot_styles import *

# %%

language = "fr"

polities_dtf = pd.read_csv(s2_polities_list_csv)
# restore hds id to their proper str format
polities_dtf.hds_article_id = polities_dtf.hds_article_id.apply(lambda id: str(id))
polities_dtf.hds_article_id = polities_dtf.hds_article_id.apply(lambda id: ((6-len(id))*"0")+id)
polities_dtf.typology[polities_dtf.typology.isna()] = None
polities_dtf.geoidentifier[polities_dtf.geoidentifier.isna()] = None

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


