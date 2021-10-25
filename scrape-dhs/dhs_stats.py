# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dhs_scraper import DhsArticle, DhsTag

# %matplotlib inline

articles_jsonl_file = "data/dhs_fr_all_articles_content.jsonl"
#articles_jsonl_file = "data/dhs_all_articles_TESTfr.jsonl"

# %%

articles = DhsArticle.load_articles_from_jsonl(articles_jsonl_file)

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


def tags_stats(articles, title=None, figure = None):
    title_starter = title+": " if title else ""
    tags = [t for a in articles for t in a.tags]

    pdtags = pd.Series(tags)
    tags_vc = pd.Series(pdtags.value_counts().values)
    tags_quantiles = pd.DataFrame([(q, tags_vc.quantile(q, interpolation="higher")) for q in quantiles], columns=["quantile", "number of articles"])
    tags_percentiles = pd.Series([tags_vc.quantile(q, interpolation="higher") for q in percentiles])

    #tags_vc.hist()

    print(f"{title_starter}Number of unique tags: {len(set(tags))}")
    print(f"{title_starter}Median number of articles per tags: {tags_vc.quantile(0.5, interpolation='higher')},"+
    f"mean: {tags_vc.mean().round(2)}")
    print(f"{tags_quantiles}")
    plt.figure(figure)
    tags_plot = tags_percentiles.plot()
    tags_plot.set(xlabel="Tag (by number of articles percentile)", ylabel="Number of articles", title = title_starter+"Number of Articles per Tag")
    #tags_plot.set_xticks([])
    return (tags_plot, tags_percentiles)

tags_stats(articles, "Whole DHS", 31)
""

# %%

tags_by_level = [
    [t.get_level(i) for t in tags]
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

def texts_stats(articles, title=None, figure=None):
    title_starter = title+": " if title else ""
    texts_length = [len(a.text) for a in articles]
    texts_length.sort(reverse=True)

    pdtl = pd.Series(texts_length)
    texts_lengths_quantiles = pd.DataFrame([(q, pdtl.quantile(q, interpolation="higher")) for q in quantiles], columns=["quantile", "number of articles"])
    pdtl_percentiles = pd.Series([pdtl.quantile(q, interpolation="higher") for q in percentiles])

    print(f"{title_starter}Number of articles: {len(articles)}")
    print(f"{title_starter}Median length of articles (character): {pdtl.quantile(0.5, interpolation='higher')},"+
    f"mean: {pdtl.mean().round(2)}")
    print(f"{texts_lengths_quantiles}")
    plt.figure(figure)
    texts_plot = pdtl_percentiles.plot()
    texts_plot.set(
        xlabel="Article (by length percentile)",
        ylabel="Article length (characters)",
        title = title_starter+"Length of Articles (character)")
    return texts_plot

texts_stats(articles, "Whole DHS",3)
""

# %%

people = [a for a in articles if a.is_person()]
non_people = [a for a in articles if not a.is_person()]

# %%

texts_stats(people, "People", 1)
texts_plot = texts_stats(non_people, "Non-people", 1)
texts_plot.set(title="Length of articles (character): People vs Non-people Articles")
texts_plot.legend(["people", "non-people"])
""

# %%


np_elites_locales = [a for a in non_people if DhsTag("Elites (jusque vers 1800) / Elites locales", "") in a.tags]


# %%

# categories: themes, people, families, spatial
categories = [
    ("themes", f"data/dhs_fr_category_themes_articles.jsonl"),
    ("people", f"data/dhs_fr_category_people_articles.jsonl"),
    ("families", f"data/dhs_fr_category_families_articles.jsonl"),
    ("spatial", f"data/dhs_fr_category_spatial_articles.jsonl")
]

empty_articles_by_category = [set(DhsArticle.load_articles_from_jsonl(c[1])) for c in categories]
articles_ids_by_category = [set(a.id for a in abc) for abc in empty_articles_by_category]
articles_by_category = [
    [a for a in articles if a.id in abyc]
    for abyc in articles_ids_by_category
]

[len(articles) for articles in empty_articles_by_category]

sarticles_ids = set(a.id for a in articles)
missing_articles = [
    a
    for abyc in empty_articles_by_category
    for a in abyc if a.id not in sarticles_ids
]

sarticles_category = set(a for c in articles_by_category for a in c)
category_missing_articles = [
    a
    for a in articles if a not in sarticles_category
]

# %%

articles_by_category_text_stats_plot=None
for i, articles_in_category in enumerate(articles_by_category):
    articles_by_category_text_stats_plot = texts_stats(articles_in_category, categories[i][0],figure=42)
articles_by_category_text_stats_plot.legend([t[0]+f" ({len(articles_by_category[i])} articles)" for i,t in enumerate(categories)])
articles_by_category_text_stats_plot.set(title="Length of Articles (character) by DHS category")


# %%

"""
todo:
- graph proportion of articles in DHS per category
- length of articles vs in/out wikidata
"""
languages = ["fr", "de", "it", "en"]

wikidata_dhs_links = pd.read_csv("../wikidata_dhs_linking/wikidata_dhs_wikipedia_articles_gndid_instanceof.csv")
articles_in_wikidata_ids = set(wikidata_dhs_links.dhsid)
articles_in_wikipedia_by_lang_ids = {lang:set(wikidata_dhs_links.dhsid[~wikidata_dhs_links[f"article{lang}"].isnull()]) for lang in languages}

# %%

def in_out_wikidata(articles, articles_ids=articles_in_wikidata_ids):
    return ([a for a in articles if a.id in articles_ids], [a for a in articles if a.id not in articles_ids])

articles_in_out_wikidata = in_out_wikidata(articles)
articles_in_out_wikidata_by_category = [in_out_wikidata(abyc) for abyc in articles_by_category]
articles_in_wikipedia_by_lang = {l: in_out_wikidata(articles, articles_in_wikipedia_by_lang_ids[l]) for l in languages}
articles_in_wikipedia_by_category_and_lang = [
    {l: in_out_wikidata(abyc, articles_in_wikipedia_by_lang_ids[l]) for l in languages}
     for abyc in articles_by_category
]

prop_articles_in_wd_by_category = [
    (
        categories[i][0],
        len(articles_in_out_wikidata_by_category[i][0]),
        len(articles_by_category[i]),
        round(len(articles_in_out_wikidata_by_category[i][0]) / float(len(articles_by_category[i])),2),
        round(len(articles_in_wikipedia_by_category_and_lang[i]["fr"][0]) / float(len(articles_by_category[i])),2),
        round(len(articles_in_wikipedia_by_category_and_lang[i]["de"][0]) / float(len(articles_by_category[i])),2),
        round(len(articles_in_wikipedia_by_category_and_lang[i]["it"][0]) / float(len(articles_by_category[i])),2),
        round(len(articles_in_wikipedia_by_category_and_lang[i]["en"][0]) / float(len(articles_by_category[i])),2),
    ) for i in range(len(articles_by_category))
]
prop_articles_in_wd_by_category = pd.DataFrame(
    prop_articles_in_wd_by_category,
    columns = ["category", "nb_in_wd", "total", "prop_in_wd", "prop_in_fr_wk", "prop_in_de_wk", "prop_in_it_wk", "prop_in_en_wk"]
)
prop_articles_in_wd_by_category.set_index("category", inplace=True)

percent_articles_in_wd_by_category = prop_articles_in_wd_by_category.loc[:,["prop_in_wd", "prop_in_de_wk", "prop_in_fr_wk", "prop_in_en_wk", "prop_in_it_wk"]].apply(lambda x: x*100)
percent_articles_in_wd_by_category
percent_articles_in_wd_by_category_plot = percent_articles_in_wd_by_category.plot.bar()
percent_articles_in_wd_by_category_plot.legend([f"% in {lng}" for lng in ["Wikidata", "DE Wikipedia", "FR Wikipedia", "EN Wikipedia", "IT Wikipedia"]])
percent_articles_in_wd_by_category_plot.set(title = "Proportion of DHS articles, by category, covered in different languages of wikipedia", ylabel="%")

print(f"""Proportion of DHS articles, by category, covered in different languages of wikipedia:
{prop_articles_in_wd_by_category}
Conclusion:
- Lots of entities are in WikiData, but not that many in Wikipedia.
- Articles on spatial themes are very well covered in wikipedia.
- families are very badly covered in wikipedia.
- DE wikipedia has a substantial better coverage of DHS articles.
""")
#prop_articles_in_wd_by_category

# %% Articles length by presence in WD or not

articles_in_out_wikidata_text_stats_plot = texts_stats(articles_in_out_wikidata[0], figure=5673)
texts_stats(articles_in_out_wikidata[1], figure=5673)
articles_in_out_wikidata_text_stats_plot.legend([f"Articles in Wikidata ({len(articles_in_out_wikidata[0])} articles)", f"Articles not in Wikidata ({len(articles_in_out_wikidata[1])} articles)"])
articles_in_out_wikidata_text_stats_plot.set(title="Length of Articles (character) depending on Presence in Wikidata")

# %% Articles length by presence in DE WK or not


articles_in_out_dewk_text_stats_plot = texts_stats(articles_in_wikipedia_by_lang["de"][0], figure=9322)
texts_stats(articles_in_wikipedia_by_lang["de"][1], figure=9322)
articles_in_out_dewk_text_stats_plot.legend([f"Articles in DE Wikipedia ({len(articles_in_wikipedia_by_lang['de'][0])} articles)", f"Articles not in DE Wikipedia ({len(articles_in_wikipedia_by_lang['de'][1])} articles)"])
articles_in_out_dewk_text_stats_plot.set(title="Length of Articles (character) depending on Presence in DE Wikipedia")


# %% Articles length by category and presence in DE WK or not



# %%


# %%
