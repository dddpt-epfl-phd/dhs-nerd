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
spatial_articles = articles_by_category["spatial"]

# %%

stats_articles_by_category_proportions = tag_tree.stats_articles_by_category_proportions_curry(articles_ids_by_category, DHS_ARTICLE_CATEGORIES)
# %%
# %%

#json_dump_tag_tree(tag_tree_all, "all")


# %%


spatial_tags = [t for a in spatial_articles for t in a.tags]
spatial_utags = set(t for t in spatial_tags)

spatial_tag_tree = tag_tree.build_tag_tree(spatial_utags)
tag_tree.add_articles_to_tag_tree(spatial_tag_tree, spatial_articles)
tag_tree.compute_nodes_statistics(spatial_tag_tree, stat_func=stats_articles_by_category_proportions, stat_aggregator_func=tag_tree.stats_aggregator_articles_by_category_proportions)
""
#json_dump_tag_tree(spatial_tag_tree, "spatial")

# %%


"""
TODO creation list of entities to extract

todo:
- list all tags relevant to create a spatial entity
    commune, ancienne commune, baillage, seigneurie, etc
- list all spatial entities
- make 1 entry per relevant spatial entity tag

"""


# %%


polities_tags_names = [
    # Entités politiques
    "Entités politiques / District",
    "Entités politiques / Comté, landgraviat",
    "Entités politiques / Canton",
    "Entités politiques / Seigneurie",
    "Entités politiques / Ancienne commune",
    "Entités politiques / Bailliage, châtellenie",
    "Entités politiques / Etat historique disparu",
    "Entités politiques / Canton, Département, République (1790-1813)",
    "Entités politiques / Commune",
    "Entités politiques / Ancien district",
    "Entités politiques / Ville, commune, localité (étranger)",

    # Entités ecclésiastiques
    'Entités ecclésiastiques / Abbaye, couvent, monastère, prieuré',
    "Entités ecclésiastiques / Commanderie",
    "Entités ecclésiastiques / Chapitre cathédral",
    "Entités ecclésiastiques / Archidiocèse",
    "Entités ecclésiastiques / Evêché, diocèse",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

future_polities_tags_names = [
    # Thurgau
    # TG is a fishfest of fun regarding municipal subunits
    # doable but needs dedicated handling
    "Entités politiques / Munizipalgemeinde (TG)",
    "Entités politiques / Ortsgemeinde (TG)",

    # Habitat infracommunal
    # really small entities, do we have geometries?
    # is it easily possible to map them?
    "Habitat infracommunal / Village, hameau, fraction, localité, ferme"
]

discutable_polities_tags_names = [
    "Entités politiques / Territoire (étranger)",
    "Entités politiques / Ville médiévale",
    "Entités politiques / Etat (étranger); continent, partie de continent",
    "Entités politiques / Communauté, collectivité",
]


# %%

"""


information for each tag:
- tag name
- facet
- polities_extraction_rule (taken, not taken, to investigate, future)
- discussion (why such assignment?)
- random notes
"""

empty_node_line = {
        "depth": "",
        "short_name": "",
        "name": "",
        "facet": "",
        "nb_articles": "",
        "polities_extraction_rule": "",
        "discussion": "" ,
        "notes": ""
}
basis_line_returns=2
def name_to_short_name(n):
    return n.split("/")[-1].strip()

def tag_tree_node_to_polities_to_extract_json_template(node, children_json):
    lvl = len(node["facet"].split(".")) if node["facet"] is not None else 0
    print("\n\nnode name")
    print(node["full_name"] if node["full_name"] is not None else node["name"])
    print("(basis_line_returns-lvl):")
    print((basis_line_returns-lvl))
    name = node["full_name"] if node["full_name"] is not None else node["name"]
    node_line = {
        "depth": lvl,
        "short_name": name_to_short_name(name),
        "name": name,
        "facet": node["facet"],
        "nb_articles": len(node["articles"]) if len(node["articles"])>0 else "",
        "polities_extraction_rule": "" if len(node["articles"])>0 else "-",
        "discussion": "" if len(node["articles"])>0 else "-",
        "notes": "" if len(node["articles"])>0 else "-",
    } if len(node["total_statistics"]["spatial"])>0 else None
    return [
        n for n in
        [node_line] + [j for children_list in children_json for j in children_list]
        if n is not None
    ] + (max(basis_line_returns-lvl,0) * [empty_node_line])

polities_to_extract_json_template = tag_tree.traverse_depth_first(spatial_tag_tree, tag_tree_node_to_polities_to_extract_json_template)
# %%

polities_to_extract = pd.DataFrame(polities_to_extract_json_template)
polities_to_extract.to_csv(s2_s1_polities_tags_extraction_rules, index=False)
polities_to_extract
# %%
pd.set_option('display.max_rows', None)
tags_to_extract = pd.read_csv(s2_s1_polities_tags_extraction_rules_hand_filled)
tags_to_extract = tags_to_extract.loc[~tags_to_extract.depth.isna()]
tags_to_extract.nb_articles[tags_to_extract.nb_articles.isna()] = 0
tags_to_extract["dhstag"] = tags_to_extract.name.apply(lambda n: DhsTag(n))
tags_to_extract["short_name"] = tags_to_extract.name.apply(name_to_short_name)
tags_to_extract_reordered_columns = set(["depth", "name", "short_name"])
tags_to_extract = tags_to_extract[["depth", "short_name"] + [c for c in tags_to_extract.columns if c not in tags_to_extract_reordered_columns] +["name"]]
tags_to_extract

selected_tags_dtf = tags_to_extract.loc[tags_to_extract["polities_extraction_rule"]=="oui"]
selected_tags_dtf = selected_tags_dtf.sort_values(["level","nb_articles"],ascending=False)


# %%

selected_tags = set(selected_tags_dtf["dhstag"])
selected_tags
for t in selected_tags:
    print(t.tag)

# %%

selected_articles = [(a,[t for t in a.tags if t in selected_tags]) for a in spatial_articles]
selected_articles = [(*sa,len(sa[1])) for sa in selected_articles if len(sa[1])>0]
selected_articles_dict = {a: (tags, nbtags) for (a, tags, nbtags) in selected_articles}
unselected_articles = [(a.id,a.title) for a in spatial_articles if a not in selected_articles_dict]
selected_articles_dtf = pd.DataFrame([
    (a.id+f"-{i}", a.title, t, nbtags, a.id)
    for a, tags, nbtags in selected_articles
    for i,t in enumerate(sorted(tags, key=lambda t: t.tag))
], columns=["entity_id", "title", "tag", "nbtags", "hds_id"])

# %%
spatial_utags
selected_articles_per_tag = [(
        t,
        t in selected_tags,
        [a for a in tag_articles if a in selected_articles_dict],
        [a for a in tag_articles if a not in selected_articles_dict],
        tag_articles
    ) for t, tag_articles in  articles_per_tag
    if t in spatial_utags
]
selected_articles_per_tag_dtf = pd.DataFrame(selected_articles_per_tag,  columns = ["tag", "is_tag_selected", "selected_articles", "refused_articles", "all_tag_articles"])
selected_articles_per_tag_dtf["selected_articles"] = selected_articles_per_tag_dtf.selected_articles.apply(len)
selected_articles_per_tag_dtf["refused_articles"] = selected_articles_per_tag_dtf.refused_articles.apply(len)
selected_articles_per_tag_dtf["all_tag_articles"] = selected_articles_per_tag_dtf.all_tag_articles.apply(len)
selected_articles_per_tag_dtf["coverage"] = selected_articles_per_tag_dtf.selected_articles / selected_articles_per_tag_dtf.all_tag_articles
selected_articles_per_tag_dtf["nb_resulting_entities"] = selected_articles_per_tag_dtf.is_tag_selected * selected_articles_per_tag_dtf.selected_articles
selected_articles_per_tag_dtf.head()

selected_articles_per_tag_dtf.coverage.describe()

# %%

print("total nb of entities:")
print(selected_articles_dtf.shape[0])
print("representing articles:")
print(len(selected_articles_dtf.hds_id.unique()))
# %%

# investingating whether villes médiévales deserve to be included?
ville_med = DhsTag("Entités politiques / Ville médiévale")
selected_articles_per_tag_dtf.loc[selected_articles_per_tag_dtf.tag==ville_med]
vmtag = [t for t in selected_articles_per_tag if t[0]==ville_med][0]
ville_med = vmtag[0]
[(a.id,a.title) for a in vmtag[3]]
# -> there are 4 destroyed villes médiévales
# -> interesting historically, but not exploitable GIS wise, ok to exclude them

# %%


selected_tags_by_lvl = selected_tags_dtf.groupby(selected_tags_dtf.level).aggregate("sum")[["nb_articles"]]
selected_tags_by_lvl
# %%

selected_tags_dtf[["short_name","level","nb_articles"]]

# %%

relationship_nb_estimation_low = [
    (10, 3),
    (20, 3),
    (30, 3),
    (40, 2),
]

relationship_nb_estimation_mid = [
    (10, 5),
    (20, 3),
    (30, 3),
    (40, 2),
]

relationship_nb_estimation_high = [
    (10, 6),
    (20, 5),
    (30, 4),
    (40, 3),
]

relationship_nb_estimations = [
    ("nb_rel_low", relationship_nb_estimation_low),
    ("nb_rel_mid", relationship_nb_estimation_mid),
    ("nb_rel_high", relationship_nb_estimation_high)
]

# Estimation rules for relationships
def relationship_nb_estimator(lvl, relationship_nb_estimation):
    for threshold, nb_relationships in relationship_nb_estimation:
        if lvl<=threshold:
            return nb_relationships

def add_nb_rel_estimation_to_dtf(dtf, col_name, relationship_nb_estimation):
    dtf[col_name] = [r[1].nb_articles * relationship_nb_estimator(r[0], relationship_nb_estimation)  for r in dtf.iterrows()]
def add_nb_rel_estimations_to_dtf(dtf, estimations):
    for col_name, estimation in estimations:
        add_nb_rel_estimation_to_dtf(dtf, col_name, estimation)
    
add_nb_rel_estimations_to_dtf(selected_tags_by_lvl, relationship_nb_estimations)
selected_tags_by_lvl
# %%
nb_things_to_extract = selected_tags_by_lvl.aggregate(sum).to_frame("nb_things")
# -> ~20k relations to extract, gargl...
nb_things_to_extract
# %%

"""
Now let's go to time-estimations:
"""

minutes_per_entity ={
    "low": 5,
    "mid": 10,
    "high": 20
}
minutes_per_relation ={
    "low": 5,
    "mid": 10,
    "high": 20
}

def add_time_estimation(dtf, est_lvl_ent, est_lvl_rel):
    colname_basis = "rel"+est_lvl_rel+"_ent"+est_lvl_ent
    colname_h = colname_basis+"_h"
    colname_d = colname_basis+"_d"
    colname_wy = colname_basis+"_wy"
    dtf[colname_h] = minutes_per_relation[est_lvl_rel]*dtf.nb_things / 60
    dtf[colname_h][0] = dtf.nb_things[0] * minutes_per_entity[est_lvl_ent] / 60
    dtf[colname_h][1:] +=dtf[colname_h][0]
    dtf[colname_d] = dtf[colname_h] / 8
    dtf[colname_wy] = dtf[colname_d] / 200
    dtf = dtf.round(1)
    return dtf

nb_things_to_extract = add_time_estimation(nb_things_to_extract,"low","low")
nb_things_to_extract = add_time_estimation(nb_things_to_extract,"mid","mid")
nb_things_to_extract = add_time_estimation(nb_things_to_extract,"high","high")

nb_things_to_extract

# %%
