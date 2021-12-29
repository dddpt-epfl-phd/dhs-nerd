# %%


import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle

from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S4_JSONL_ALL_ARTICLES_LINKED_FILE, localize
# %%
"""


Steps:
1) for each link get:
    - origin: original-dhs, entity-fishing
    - dhsid
    - wk page id
    - article
    - year of article
2) for each article get:
    - character count
    - year of version
    - nb of text_links
        - from original-dhs
        - from ef total
        - from ef to DHS
        - from ef to WK only
        - from ef to WD only
        - unlinked
"""



# %%


def get_dhsid(text_link):
    return text_link.get("dhsid")
def get_wikidata_url(text_link):
    annotation = text_link.get("annotation")
    if annotation is not None:
        return annotation.get("wikidata_entity_url")
def get_wikipedia_page_id(text_link):
    annotation = text_link.get("annotation")
    if annotation is not None:
        return annotation.get("wikipedia_page_id")

ORIGIN_FROM_ENTITY_FISHING = "entity_fishing"
ORIGIN_FROM_DHS = "original_dhs"
def get_origin(text_link):
    origin = text_link.get("origin")
    if origin is None:
        return ORIGIN_FROM_DHS
    return origin

# %%

lng="fr"
languages = ["fr","de"]
max_nb_articles=1000



linked_articles = {
    lng: list(DhsArticle.load_articles_from_jsonl(
        localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE,lng)
        #indices_to_keep=[i for i in range(max_nb_articles)]
    )) for lng in languages
}


# %%


def article_text_links_stats(article: DhsArticle):
    from_dhs = set()
    from_ef = set()
    to_dhs = set()
    to_wk = set()
    to_wd = set()
    nb_unlinked = 0
    for text_block in article.text_links:
        for tl in text_block:
            origin = get_origin(tl)
            dhsid = get_dhsid(tl)
            if origin==ORIGIN_FROM_DHS:
                from_dhs.add(dhsid)
            elif origin==ORIGIN_FROM_ENTITY_FISHING:
                wd_url = get_wikidata_url(tl)
                wk_page = get_wikipedia_page_id(tl)
                from_ef.add(wd_url)    
                if dhsid is not None:
                    to_dhs.add(dhsid)
                elif wd_url is not None:
                    to_wd.add(wd_url)
                elif wk_page is not None:
                    to_wk.add(wk_page)
                else:
                    nb_unlinked+=1
    return {
        "dhsid": article.id,
        "year": int(article.version[0:4]),
        "nb_char": len(article.text),
        "nb_from_dhs": len(from_dhs),
        "nb_from_ef": len(from_ef),
        "nb_to_dhs": len(to_dhs),
        "nb_to_wd": len(to_wd),
        "nb_to_wk": len(to_wk),
        "nb_to_dhs_wd": len(to_wd)+len(to_dhs),
        "nb_unlinked": nb_unlinked,
    }

# %%

links_stats_per_article = {
    lng: pd.DataFrame([article_text_links_stats(a) for a in linked_articles[lng]])
    for lng in languages
}
links_stats_per_article["fr"]


# %%

links_stats_per_article["fr"].describe()

# %%

aarau = [a for a in linked_articles["fr"] if a.id=="001620"][0]
#[tl.get("origin") for tb in aarau.text_links for tl in tb]

# %%
for lng in languages:
    links_stats_per_article[lng]["nb_articles"] = 1

links_stats_per_year = {
    lng: links_stats_per_article[lng].groupby("year").sum()
    for lng in languages
}


# %%

plt.figure(42)
nb_articles_per_year_plot_fr = links_stats_per_year["fr"]["nb_articles"].plot()
plt.figure(42)
nb_articles_per_year_plot_de = links_stats_per_year["de"]["nb_articles"].plot()
nb_articles_per_year_plot_de.legend(["French HDS","German HDS"])
nb_articles_per_year_plot_de.set(
    title = "Number of HDS articles whose last version is in year",
    xlabel="Year",
    ylabel="# of articles",
)

# %%

links_stats_per_article["fr"].groupby("year").get_group(2001).describe()


# %%

def plot_nb_per_year(dtf, col="nb_from_dhs", denominator_col="nb_articles",figure=None, multiplier_factor=1):
    new_col = col+"_per_"+denominator_col 
    dtf[new_col] = dtf[col] / dtf[denominator_col] * multiplier_factor
    plt.figure(figure)
    return dtf[new_col].plot()

# %%

plot_nb_per_year(links_stats_per_year["fr"], figure=34)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["de"], figure=34)
nb_from_dhs_per_article_per_year_plot.legend(["French HDS","German HDS"])
nb_from_dhs_per_article_per_year_plot.set(
    title = "Average number of links per article per year in the HDS",
    xlabel="Year",
    ylabel="# of links per article",
)


# %%

nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["fr"], denominator_col="nb_char", figure=36, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["de"], denominator_col="nb_char", figure=36, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot.legend(["French HDS","German HDS"])
nb_from_dhs_per_article_per_year_plot.set(
    title = "Average number of links per 1000 characters per year in the HDS",
    xlabel="Year",
    ylabel="# of links per 1000 characters",
)
# %%

nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["fr"], denominator_col="nb_char", figure=37, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["de"], denominator_col="nb_char", figure=37, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["fr"], col="nb_to_dhs_wd",denominator_col="nb_char", figure=37, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["de"], col="nb_to_dhs_wd", denominator_col="nb_char", figure=37, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["fr"], col="nb_to_dhs",denominator_col="nb_char", figure=37, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot = plot_nb_per_year(links_stats_per_year["de"], col="nb_to_dhs", denominator_col="nb_char", figure=37, multiplier_factor=1000)
nb_from_dhs_per_article_per_year_plot.legend([
    "Original HDS links FR","Original HDS links DE",
    "Wikidata links from entity-fishing FR", "Wikidata links from entity-fishing DE",
    "HDS Links from entity-fishing FR", "HDS Links from entity-fishing DE"
])
nb_from_dhs_per_article_per_year_plot.set(
    title = "Average number of links per 1000 characters per year in the HDS",
    xlabel="Year",
    ylabel="# of links per 1000 characters",
)
# %%




labels = ["Original HDS links", "Links from entity-fishing"]
nb_links_plot_lng = "de"
denominator = links_stats_per_article[nb_links_plot_lng].nb_char.sum() / 1000
totals_to_dhs = [links_stats_per_article[nb_links_plot_lng].nb_from_dhs.sum()/denominator, links_stats_per_article[nb_links_plot_lng].nb_to_dhs.sum()/denominator]
totals_to_wk = [0, links_stats_per_article[nb_links_plot_lng].nb_to_wd.sum()/denominator]
width = 0.35       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(figsize=(4,5))

ax.bar(labels, totals_to_dhs, label='Links to DHS', width=width)
ax.bar(labels, totals_to_wk, bottom=totals_to_dhs,label='Links to Wikidata/pedia', width=width)
ax.set(
    title='Number of links in original HDS and found by entity-fishing',
    ylabel=" # links per 1000 characters"
)
ax.legend()

plt.show()

# %%

# %%
