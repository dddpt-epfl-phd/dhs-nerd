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

import os
print("cwd:")
print(os.getcwd())

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from data_file_paths import S0_JSONL_ALL_ARTICLES_PARSED_FILE, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES, localize, s2_s1_polities_tags_extraction_rules, s2_s1_polities_tags_extraction_rules_hand_filled
from plot_styles import *

# %matplotlib inline

language="fr"
articles_jsonl_file = localize(S0_JSONL_ALL_ARTICLES_PARSED_FILE, language)
#articles_jsonl_file = "data/dhs_all_articles_TESTfr.jsonl"

# %%

articles = list(DhsArticle.load_articles_from_jsonl(articles_jsonl_file))


# %%


# Links from "en bref" section wrongly caught as a tag
zve_bug = [a for a in articles if DhsTag("Zwyer von Evibach", "Z=vE") in a.tags]
if len(zve_bug)>0:
    print(f"zve_bug.id: {zve_bug[0].id}")


# %%
tags = [t for a in articles for t in a.tags]
# remove error tag ArticleMetadataSheet from HeidiDeneys article: https://hls-dhs-dss.ch/fr/articles/058046/2019-06-12/
tags = [t for t in tags if "ArticleMetadataSheet" not in t.tag]

tags_start = set(t.url[0:10] for t in tags)
tags_start
# -> only 2 possible starts, remove all the article ones!

# %%

# correct for tags that aren't actually tags...
false_tags = [t for t in tags if t.url.startswith("/articles")]
tags = [t for t in tags if not t.url.startswith("/articles")]
for a in articles:
    a.tags = [t for t in a.tags if not t.url.startswith("/articles")]
    # remove error tag ArticleMetadataSheet from HeidiDeneys article: https://hls-dhs-dss.ch/fr/articles/058046/2019-06-12/
    a.tags = [t for t in a.tags if "ArticleMetadataSheet" not in t.tag]

# %%

utags_names = set(t.tag for t in tags)
utags_facets = set(t.facet for t in tags)
utags_names_facets = set((t.tag, t.facet) for t in tags)

utags = set(tags)
(len(utags), len(utags_names), len(utags_facets), len(utags_names_facets))


# %%

quantiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1]
percentiles = np.arange(0,1.005,0.01)

# %%




articles_per_tag = DhsTag.get_articles_per_tag(articles)



# %%

empty_articles_by_category = {c:set(DhsArticle.load_articles_from_jsonl(localize(f, language))) for c,f in S0_JSONL_ARTICLES_BY_CATEGORIES_FILES.items()}
articles_ids_by_category = {c:set(a.id for a in abc) for c,abc in empty_articles_by_category.items()}
articles_by_category = {
    c:set([a for a in articles if a.id in abyc])
    for c,abyc in articles_ids_by_category.items()
}
people_articles = articles_by_category["people"]

# %%



# %%
medieval_facets = [ # not fiable
    "3/000100.121100", # tag "Politique / Société (1250-1800)"
    "2/000100.120000", # tag "Politique / Société (jusqu'en 1250)"
    "000300", # tag "Elites (jusque vers 1800)"
]

medieval_tags_start = [
    "Politique / Société (jusqu'en 1250)",
    "Politique / Société (1250-1800)",
    "Elites (jusque vers 1800)"    
]
# %%

medieval_tags_facet = [t for t in utags if any(t.facet.startswith(f) for f in medieval_facets)]
medieval_tags = {t for t in utags if any(t.tag.startswith(f) for f in medieval_tags_start)}

# %%
len(medieval_tags)
# %%

medieval_tags_dtf = pd.DataFrame([(t, len([a for a in people_articles if t in a.tags])) for t in medieval_tags], columns=["tag","nb_articles"]).sort_values(by="nb_articles",ascending=False)
medieval_tags_dtf

# %%

top_med_tags = list(medieval_tags_dtf.iloc[0:15].tag)

# %%

medieval_people = [a for a in people_articles if any(t in a.tags for t in medieval_tags)]
len(medieval_people)
# %%

# %%


def get_companion_tags_statistic(articles, tag):
    articles_with_tag = [a for a in articles if tag in a.tags]
    companion_tags = set([t for a in articles_with_tag for t in a.tags])
    return pd.DataFrame({
        "tag": [t.tag[10:30]+" .. "+t.tag[-25:] for t in companion_tags],
        "nb": [len([a for a in articles_with_tag if t in a.tags]) for t in companion_tags],
        "prop": [len([a for a in articles_with_tag if t in a.tags])/len(articles_with_tag) for t in companion_tags],
        "articles": [[a.id for a in articles_with_tag if t in a.tags] for t in companion_tags]
    }).sort_values("nb", ascending=False)

# %%

get_companion_tags_statistic(medieval_people, top_med_tags[1])

# %%

hnoblesse = [t for t in utags if t.tag=="Politique / Société (jusqu'en 1250) / Moyen Age (1000-1250) / Haute noblesse"][0]
dynasties_after1250 = [t for t in utags if t.tag=="Politique / Société (1250-1800) / Politique étrangère / Dynasties"][0]
get_companion_tags_statistic(medieval_people, dynasties_after1250)

# %%

articles_dyn_after1250 = [(a.id,a.title) for a in people_articles if dynasties_after1250 in a.tags]
articles_dyn_after1250

# %%

