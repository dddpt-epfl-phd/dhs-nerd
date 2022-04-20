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
from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S0_JSONL_ALL_ARTICLES_PARSED_FILE, S0_DHS_CATEGORIES, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES, s0_png_articles_lengths_by_category_figure, s0_png_percent_articles_in_wd_by_category, localize, S1_WIKIDATA_DHS_WIKIPEDIA_LINKS, s2_s0_tag_tree_with_ids_web, s2_s0_tag_tree_with_ids
from plot_styles import *

# %matplotlib inline

language="fr"
articles_jsonl_file = localize(S0_JSONL_ALL_ARTICLES_PARSED_FILE, language)
#articles_jsonl_file = "data/dhs_all_articles_TESTfr.jsonl"

# %%

articles = list(DhsArticle.load_articles_from_jsonl(articles_jsonl_file))

"""
Questions to answer:
- what are the tags related to spatial articles?
    -> what's their distribution?
    -> tag co-occurence?
- are non-leaf tags used to tag articles?


"""

# %%


# Links from "en bref" section wrongly caught as a tag
zve_bug = [a for a in articles if DhsTag("Zwyer von Evibach", "") in a.tags]
if len(zve_bug)>0:
    print(f"zve_bug.id: {zve_bug[0].id}")


# %%
tags = [t for a in articles for t in a.tags]

tags_start = set(t.url[0:10] for t in tags)
tags_start
# -> only 2 possible starts, remove all the article ones!

# %%

# correct for tags that aren't actually tags...
false_tags = [t for t in tags if t.url.startswith("/articles")]
tags = [t for t in tags if not t.url.startswith("/articles")]
for a in articles:
    a.tags = [t for t in a.tags if not t.url.startswith("/articles")]

# %%

utags = set(t for t in tags)
len(utags)


# %%

quantiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1]
percentiles = np.arange(0,1.005,0.01)

# %%


def tags_stats(articles, title=None, figure = None, **plot_kwargs):
    title_starter = title+": " if title else ""
    tags = [t for a in articles for t in a.tags]

    pdtags = pd.Series(tags)
    tags_vc = pd.Series(pdtags.value_counts().values)
    tags_quantiles = pd.DataFrame([(q, tags_vc.quantile(q, interpolation="higher")) for q in quantiles], columns=["quantile", "number of articles"])
    tags_percentiles = pd.Series([tags_vc.quantile(q, interpolation="higher") for q in percentiles])

    #tags_vc.hist()

    print(f"{title_starter}Number of unique tags: {len(set(tags))}")
    print(f"{title_starter}Median number of articles per tags: {tags_vc.quantile(0.5, interpolation='higher')},"+
    f"mean: {tags_vc.mean()}")#".round(2)}")
    print(f"{tags_quantiles}")
    plt.figure(figure)
    tags_plot = tags_percentiles.plot(**plot_kwargs)
    tags_plot.set(xlabel="Tag (by number of articles percentile)", ylabel="Number of articles", title = title_starter+"Number of Articles per Tag")
    #tags_plot.set_xticks([])
    return (tags_plot, tags_percentiles)

tags_stats(articles, "Whole HDS", 31, color=colors_by_language[language])
""

# %%

tags_by_level = [
    [t.get_level(i) for t in tags if t.get_level(i) is not None]
    for i in range(5)
]
tags_by_level[4] = [t.get_level(111, True) for t in tags]
utags_by_level = [set(ts) for ts in tags_by_level]
pdtags_by_level = [pd.Series(ts) for ts in tags_by_level]

tags_by_level_vc = [
    pdts.value_counts()
    for pdts in pdtags_by_level
]

tags_by_level_quantiles = [
    [pdts.quantile(q, interpolation="higher") for q in quantiles]
    for pdts in tags_by_level_vc
]
# %%


princes_eveques_tag = [t for t in utags if "Princes-évêques" in t.tag][0]
princes_eveques_articles = [a for a in articles if princes_eveques_tag in a.tags]

[(a.title, a.url) for a in princes_eveques_articles]
# %%

articles_per_tag = DhsTag.get_articles_per_tag(articles)

# %%
with open( "dhsids_per_tag.json", "w") as f:
    json.dump([
        (t.tag, t.url, [a.id for a in articles])
        for t, articles in articles_per_tag
    ], f)

# %%

def json_dump_tag_tree(tag_tree_root, name, article_to_json_func=lambda a: (a.title, a.id)):
    article_revert_json_func = tag_tree.modify_articles(tag_tree_root, article_to_json_func)
    for tag_tree_json in [s2_s0_tag_tree_with_ids, s2_s0_tag_tree_with_ids_web]:
        with open( tag_tree_json.replace("<CASE>", name), "w") as f:
            json.dump(tag_tree_root, f, ensure_ascii=False)
    article_revert_json_func()

# %%

#stats_articles_by_category_proportions = tag_tree.stats_articles_by_category_proportions_curry(articles_by_category, DHS_ARTICLE_CATEGORIES)

tag_tree_all = DhsTag.build_tag_tree(utags)
tag_tree.add_articles_to_tag_tree(tag_tree_all, articles_per_tag=articles_per_tag)
tag_tree.traverse_depth_first(tag_tree_all, tag_tree.recursive_node_statistics)

# %%

json_dump_tag_tree(tag_tree_all, "all")

# %%

empty_articles_by_category = {c:set(DhsArticle.load_articles_from_jsonl(localize(f, language))) for c,f in S0_JSONL_ARTICLES_BY_CATEGORIES_FILES.items()}
articles_ids_by_category = {c:set(a.id for a in abc) for c,abc in empty_articles_by_category.items()}
articles_by_category = {
    c:[a for a in articles if a.id in abyc]
    for c,abyc in articles_ids_by_category.items()
}
spatial_articles = articles_by_category["spatial"]

# %%


spatial_tags = [t for a in spatial_articles for t in a.tags if not t.url.startswith("/articles")]
spatial_utags = set(t for t in tags)

spatial_tag_tree = DhsTag.build_tag_tree(spatial_utags)
tag_tree.add_articles_to_tag_tree(spatial_tag_tree, spatial_articles)

json_dump_tag_tree(spatial_tag_tree, "spatial")

# %%


# %%

# %%

# %%
