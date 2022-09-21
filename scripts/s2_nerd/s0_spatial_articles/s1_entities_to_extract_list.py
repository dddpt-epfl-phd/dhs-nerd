# started with file script s0_scrape_dhs/s0_scrape_dhs/s2_dhs_stats.py as basis

# %%
import csv
import json
from langcodes import tag_match_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from data_file_paths import S0_JSONL_ALL_ARTICLES_PARSED_FILE, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES, localize, s2_s1_polities_tags_extraction_rules, s2_s1_polities_tags_extraction_rules_hand_filled
from plot_styles import *
from f_polities_to_extract_rules import *

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
    commune, ancienne commune, bailliage, seigneurie, etc
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

def tag_tree_node_to_tags_tags_extraction_rules_annotation_dtf_row(node, children_json):
    lvl = len(node["facet"].split(".")) if node["facet"] is not None else 0
    print("\n\nnode name")
    print(node["full_name"] if node["full_name"] is not None else node["name"])
    print("(basis_line_returns-lvl):")
    print((basis_line_returns-lvl))
    name = node["full_name"] if node["full_name"] is not None else node["name"]
    node_line = {
        "depth": lvl,
        "short_name": tag_name_to_short_name(name),
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

# %%

tags_extraction_rules_annotation_dtf = pd.DataFrame(tag_tree.traverse_depth_first(spatial_tag_tree, tag_tree_node_to_tags_tags_extraction_rules_annotation_dtf_row))
tags_extraction_rules_annotation_dtf.to_csv(s2_s1_polities_tags_extraction_rules, index=False)
tags_extraction_rules_annotation_dtf
# %%
pd.set_option('display.max_rows', None)

tags_extraction_rules = get_polities_tags_extraction_rules_hand_filled()

selected_tags_dtf = get_selected_tags_dtf(tags_extraction_rules)

# %%

articles_per_tag_distrib = selected_tags_dtf.loc[:,["short_name","pct_entities"]].set_index("short_name").round(2)
ax = articles_per_tag_distrib.T.plot(kind='bar', stacked=True)
plt.legend(bbox_to_anchor=(1.1, 1.1), bbox_transform=ax.transAxes)

plt.title('Distribution of selected polities by tags')
#plt.xticks("% polities",rotation=0, ha='center')
ax.set_xticks([])
ax.set_ylabel("% polities")


# %%

# Just add a title and rotate the x-axis labels to be horizontal.

# %%

selected_tags = get_selected_tags(selected_tags_dtf)
selected_tags
for t in selected_tags:
    print(t.tag)

# %%

tagname_to_initial

# %%

selected_articles = get_selected_articles(spatial_articles, selected_tags)
selected_articles_dict = {a: (tags, nbtags) for (a, tags, nbtags) in selected_articles}
unselected_articles = [(a.id,a.title) for a in spatial_articles if a not in selected_articles_dict]
polities = get_polities_to_extract(selected_articles)

# %%

polities_dtf = get_polities_to_extract_dtf(polities, selected_tags_dtf)


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
tag_coverage_stats_dtf = pd.DataFrame(selected_articles_per_tag,  columns = ["tag", "is_tag_selected", "selected_articles", "refused_articles", "all_tag_articles"])
tag_coverage_stats_dtf["selected_articles"] = tag_coverage_stats_dtf.selected_articles.apply(len)
tag_coverage_stats_dtf["refused_articles"] = tag_coverage_stats_dtf.refused_articles.apply(len)
tag_coverage_stats_dtf["all_tag_articles"] = tag_coverage_stats_dtf.all_tag_articles.apply(len)
tag_coverage_stats_dtf["coverage"] = tag_coverage_stats_dtf.selected_articles / tag_coverage_stats_dtf.all_tag_articles
tag_coverage_stats_dtf["nb_resulting_entities"] = tag_coverage_stats_dtf.is_tag_selected * tag_coverage_stats_dtf.selected_articles
tag_coverage_stats_dtf.head()

tag_coverage_stats_dtf.coverage.describe()

# %%

print("total nb of entities:")
print(polities_dtf.shape[0])
print("representing articles:")
print(len(polities_dtf.hds_id.unique()))
# %%

# investingating whether villes médiévales deserve to be included?
ville_med = DhsTag("Entités politiques / Ville médiévale")
tag_coverage_stats_dtf.loc[tag_coverage_stats_dtf.tag==ville_med]
vmtag = [t for t in selected_articles_per_tag if t[0]==ville_med][0]
ville_med = vmtag[0]
[(a.id,a.title) for a in vmtag[3]]
# -> there are 4 destroyed villes médiévales
# -> interesting historically, but not exploitable GIS wise, ok to exclude them


# %%

selected_tags_by_lvl = selected_tags_dtf.groupby(selected_tags_dtf.level).aggregate("sum")[["nb_entities"]]
selected_tags_by_lvl["pct_entities"] = selected_tags_by_lvl.nb_entities / selected_tags_by_lvl.nb_entities.sum()*100
selected_tags_by_lvl


# %%
selected_tags_dtf[["short_name","level","nb_entities"]]

# %%

# %%

"""
Relevant graphs:
- distribution of polities into different types
- duplicated articles: distribution of nb entities per article

Relevant discussion
- specificities of HDS
    + 1-3 entities per article
- lit rev.: existing methods to handle few-shot learning
    NER:
        + Self-supervised learning (teacher-student models)
        + prototypes (classification using embedingg distance to class average)
        + Noisy Supervised Pre-training: further noisy annotations using simpler/general use model
        + Prompt based methods: formulate a question either to assign a label to a text token OR assign text tokens to a label
        + contrastive learning
    EL:
        +
- possible strategies to adress lack of training data


Proposition next steps 24.6:
- annotate 20 randomly selected articles
- ~10 communes
- 5 seigneuries
- 2 communes/seigneuries duplicates



"""




# %%

levels_descriptions = [
    (40, "Etats historiques disparus"),
    (30, "Cantons, Comtés, \nevêchés, archidiocèses, ..."),
    (25, "Cantons, Comtés, \nevêchés, archidiocèses, ..."),
    (20, "Seigneuries, bailliages, \nabbayes, districts, ..."),
    (15, "Seigneuries, bailliages, \nabbayes, districts, ..."),
    (10, "Communes")
]
levels_descriptions_dtf = pd.DataFrame(levels_descriptions, columns=["level", "label"]).set_index("level")
levels_descriptions_dtf
# %%

polities_per_main_levels = selected_tags_by_lvl.join(levels_descriptions_dtf).groupby("label").aggregate(sum).sort_values(by="nb_entities", ascending=False)

ax = polities_per_main_levels[["pct_entities"]].T.plot(kind="bar", stacked=True, width=0.2, figsize=(2,5))
plt.legend(bbox_to_anchor=(0.8, 0.8), bbox_transform=ax.transAxes)
plt.title('Distribution of polities by main categories')
#plt.xticks("% polities",rotation=0, ha='center')
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylabel("% entities")

# %%

nb_entities_per_lvl_distrib = polities_dtf.hds_id.value_counts().value_counts()
ax = plt.subplot()
plt.bar([0.5,1,1.5,2], list(nb_entities_per_lvl_distrib), width=0.3)
ax.set_xticks([0.5,1,1.5,2])
ax.set_xticklabels([1,2,3,4])


# %%

selected_tags_dtf.head()
polities_dtf.head()

max_level_per_hds_id_dtf = polities_dtf[["hds_id","level"]].groupby("hds_id").aggregate(max)
max_level_per_hds_id_dtf.rename({"level": "max_level"}, axis=1, inplace=True)
if "max_level" not in polities_dtf.columns:
    polities_dtf = polities_dtf.merge(max_level_per_hds_id_dtf, on="hds_id")

polities_dtf.head()

(polities_dtf.level!=polities_dtf.max_level).sum()

# %%

articles_per_tag_distrib.T
# %%
polities_dtf.hds_id.value_counts().head()


# %%

nb_entities_per_articles_dtf = polities_dtf.groupby("hds_id").aggregate({"level": max, "nbtags":len})
nb_entities_per_articles_dtf.sort_values(by="nbtags",inplace=True, ascending=False)
nb_entities_per_articles_dtf.head()

nb_entities_per_level_nbtags = nb_entities_per_articles_dtf.value_counts().to_frame("nb_entities")
nb_entities_per_level_nbtags = nb_entities_per_level_nbtags.reset_index().set_index("level")
nb_entities_per_level_nbtags.head()

# %%

nb_entities_per_levellabel_nbtags = nb_entities_per_level_nbtags.join(levels_descriptions_dtf).groupby(["label","nbtags"]).aggregate(sum)
nb_entities_per_levellabel_nbtags.reset_index(inplace=True)
nb_entities_per_levellabel_nbtags = nb_entities_per_levellabel_nbtags.pivot(index="nbtags", columns="label", values="nb_entities").fillna(0)
nb_entities_per_levellabel_nbtags = nb_entities_per_levellabel_nbtags[[nb_entities_per_levellabel_nbtags.columns[1],nb_entities_per_levellabel_nbtags.columns[0],nb_entities_per_levellabel_nbtags.columns[3],nb_entities_per_levellabel_nbtags.columns[2]]]


# %%

ax = nb_entities_per_levellabel_nbtags.plot(kind='bar', stacked=True)
#plt.legend(bbox_to_anchor=(1.1, 1.1), bbox_transform=ax.transAxes)
#plt.title('Distribution of selected polities by tags')
plt.title("Distribution of entities per article")
ax.set_xticklabels([1,2,3,4],rotation=0)
ax.set_ylabel("# articles")
ax.set_xlabel("# of entities per article\n\nReading: 217 articles each refer to two polities as their main subject")


# %% Loading status words dict in title

status_words_dtf = pd.read_json(s2_hds_article_titles_statuswords_hand_corrected_json)
status_words_dict = {
    r[1]["term"]: r[1]["tags"]
    for r in status_words_dtf.iterrows()
}
# %% Correcting polities titles using status words

get_dtf_titles_components(polities_dtf, status_words_dict)#["canonic_title"] = [get_canonic_title(r["polity_id"], r["article_title"], r["hds_tag"].tag, status_words_dict) for i, r in polities_dtf.iterrows()]


# %%

polities_dtf_csv = polities_dtf.copy()
polities_dtf_csv.hds_tag.apply(lambda t: t.tag)
polities_dtf_csv["hds_article_id"] = polities_dtf_csv.hds_id
del polities_dtf_csv["hds_id"]
polities_dtf_csv.hds_tag = polities_dtf_csv.hds_tag.apply(lambda t: t.tag)
columns_ordering = [
    'polity_id', 'hds_tag', 'canonic_title',
    'typology', 'toponym', 'geoidentifier',
    'hds_article_id', 'article_title', 'nbtags', 'level', 'max_level'
]
polities_dtf_csv = polities_dtf_csv[columns_ordering]
polities_dtf_csv.to_csv(s2_polities_list_csv, index=False, quoting=csv.QUOTE_NONNUMERIC)

polities_dtf_csv.head()

# %%
