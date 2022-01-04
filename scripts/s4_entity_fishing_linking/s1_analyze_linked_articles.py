# %%


import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle

from data_file_paths import *
from plot_styles import *
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

lng="fr"
languages = ["fr","de", "it"]
max_nb_articles=1000


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


def get_original_text_links(dhs_article):
    return [tl for tb in dhs_article.text_links for tl in tb if get_origin(tl)==ORIGIN_FROM_DHS]

def get_article(lng, dhsid):
    return [a for a in linked_articles[lng] if a.id==dhsid][0]

quantiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1]
percentiles = np.arange(0,1.005,0.01)

# %%




print("loading articles...")
linked_articles = {
    lng: list(DhsArticle.load_articles_from_jsonl(
        localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE,lng)
        #indices_to_keep=[i for i in range(max_nb_articles)]
    )) for lng in languages
}
print("articles loaded")

# %% understanding the missing text_links problem

alpen0 = [a for a in linked_articles["de"] if a.id =="008569"][0]

sum(len(tb) for tb in alpen0.text_links)
sum(1 for tb in alpen0.text_links for tl in tb if tl.get("origin") is None)
sum(1 for tb in alpen0.text_links for tl in tb if get_origin(tl) == ORIGIN_FROM_DHS)

print("ensuring text_links have their dhsid parsed...")
for a in linked_articles["de"]:
    #a.parse_text_links()
    for tb in a.text_links:
        for tl in tb:
            if get_origin(tl)==ORIGIN_FROM_DHS:
                l, dhsid, v = DhsArticle.get_language_id_version_from_url(tl["href"])
                tl["dhsid"] = dhsid
print("text_links dhsid parsed")



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
        "title": article.title,
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

print("computing links statistics...")
links_stats_per_article = {
    lng: pd.DataFrame([article_text_links_stats(a) for a in linked_articles[lng]])
    for lng in languages
}
links_stats_per_article["fr"]
print("links statistics done.")

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

for lng in languages:
    plt.figure(33)
    nb_articles_per_year_plot = links_stats_per_year[lng]["nb_articles"].plot(
        color = colors_by_language[lng], linestyle=linestyle_from_dhs, zorder=3
    )
nb_articles_per_year_plot.legend(["French HDS","German HDS","Italian HDS"])
nb_articles_per_year_plot.set(
    title = "Number of HDS articles whose last version is in year",
    xlabel="Year",
    ylabel="# of articles",
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)

plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_nb_articles_per_year_figure, dpi=500)
# %%

links_stats_per_article["fr"].groupby("year").get_group(2001).describe()

# %%

def normalize_col(dtf, col="nb_from_dhs", denominator_col="nb_articles", multiplier_factor=1):
    new_col = col+"_per_"+denominator_col 
    dtf[new_col] = dtf[col] / dtf[denominator_col] * multiplier_factor
    return new_col


# %%

for lng in languages:
    new_col = normalize_col(links_stats_per_year[lng])
    plt.figure(34)
    nb_from_dhs_per_article_per_year_plot = links_stats_per_year[lng][new_col].plot(
        color = colors_by_language[lng], linestyle=linestyle_from_dhs
    )
nb_from_dhs_per_article_per_year_plot.legend(["French HDS","German HDS","Italian HDS"])
nb_from_dhs_per_article_per_year_plot.set(
    title = "Average number of links per article per year in the HDS",
    xlabel="Year",
    ylabel="# of links per article",
)
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_avg_nb_links_per_article_per_year_figure, dpi=500)


# %%

for lng in languages:
    new_col = normalize_col(links_stats_per_year[lng], denominator_col="nb_char", multiplier_factor=1000)
    plt.figure(35)
    nb_from_dhs_per_1000char_per_year_plot = links_stats_per_year[lng][new_col].plot(
        color = colors_by_language[lng], linestyle=linestyle_from_dhs, zorder=3
    )
nb_from_dhs_per_1000char_per_year_plot.legend(["French HDS","German HDS","Italian HDS"])
nb_from_dhs_per_1000char_per_year_plot.set(
    title = "Number of links per 1000 characters per year in the HDS",
    xlabel="Year",
    ylabel="# of links per 1000 characters",
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_nb_links_per_1000char_per_year_figure, dpi=500)
# %%


for lng in languages:
    new_col = normalize_col(
        links_stats_per_year[lng],
        denominator_col="nb_char", multiplier_factor=1000
    )
    plt.figure(36)
    nb_per_1000char_per_year_plot = links_stats_per_year[lng][new_col].plot(
        color = colors_by_language[lng], linestyle=linestyle_from_dhs, zorder=3
    )
for lng in languages:
    new_col = normalize_col(
        links_stats_per_year[lng], col="nb_to_dhs",
        denominator_col="nb_char", multiplier_factor=1000
    )
    plt.figure(36)
    nb_per_1000char_per_year_plot = links_stats_per_year[lng][new_col].plot(
        color = colors_by_language[lng], linestyle=linestyle_from_ef_to_dhs, zorder=3
    )
for lng in languages:
    new_col = normalize_col(
        links_stats_per_year[lng], col="nb_to_dhs_wd",
        denominator_col="nb_char", multiplier_factor=1000
    )
    plt.figure(36)
    nb_per_1000char_per_year_plot = links_stats_per_year[lng][new_col].plot(
        color = colors_by_language[lng], linestyle=linestyle_from_ef_to_wkwd, zorder=3
    )
nb_per_1000char_per_year_plot.legend(
    ["Original HDS links "+lng.upper() for lng in languages] + \
    ["HDS Links from entity-fishing "+lng.upper() for lng in languages] + \
    ["All Links from entity-fishing "+lng.upper() for lng in languages]
)
nb_per_1000char_per_year_plot.set(
    title = "Number of links per 1000 characters per year in the HDS, compared with entity-fishing links",
    xlabel="Year",
    ylabel="# of links per 1000 characters",
    ylim=(0,30)
)

plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_nb_hds_ef_links_per_1000char_per_year_figure, dpi=500)
# %%




labels = [
    "FR HDS",
    "DE HDS",
    "FR entity-fishing",
    "DE entity-fishing"
]
#nb_links_plot_lng = "de"
denominator_fr = links_stats_per_article["fr"].nb_char.sum() / 1000
denominator_de = links_stats_per_article["de"].nb_char.sum() / 1000
totals_to_dhs = [
    links_stats_per_article["fr"].nb_from_dhs.sum()/denominator_fr,
    links_stats_per_article["de"].nb_from_dhs.sum()/denominator_de,
    links_stats_per_article["fr"].nb_to_dhs.sum()/denominator_fr,
    links_stats_per_article["de"].nb_to_dhs.sum()/denominator_de
]
totals_to_wk = [
    0, 0,
    links_stats_per_article["fr"].nb_to_wd.sum()/denominator_fr,
    links_stats_per_article["de"].nb_to_wd.sum()/denominator_de
]
width = 0.35       # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(figsize=(4,5))

ax.bar(
    labels, totals_to_dhs, label='Links to DHS',
    width=width, color=color_to_hds
)
ax.bar(
    labels, totals_to_wk, bottom=totals_to_dhs,
    label='Links to Wikidata/pedia', width=width, color=color_to_wkwd, zorder=3
)
ax.set(
    title=f'Number of links in original HDS and found by entity-fishing',
    ylabel=" # links per 1000 characters"
)
ax.set_xticklabels(labels, rotation= 10)
ax.legend()
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)

plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_nb_links_from_hds_and_ef_figure, dpi=500)

# %%


# %%

for lng in languages:
    for col in ["nb_from_dhs", "nb_to_dhs", "nb_to_dhs_wd"]:
        normalize_col(links_stats_per_article[lng], col=col, denominator_col="nb_char", multiplier_factor=1000)

# %%

def links_stats_distribution(links_stats, col, title=None, figure=None, **plot_kwargs):
    title_starter = title+": " if title else ""
    values = [x for x in links_stats[col]]
    values.sort(reverse=True)

    pd_values = pd.Series(values)
    values_quantiles = pd.DataFrame([(q, pd_values.quantile(q, interpolation="higher")) for q in quantiles], columns=["quantile", "number of articles"])
    pdtl_percentiles = pd.Series([pd_values.quantile(q, interpolation="higher") for q in percentiles])

    print(f"{title_starter}Number of entries: {len(links_stats)}")
    print(f"{title_starter}Median value of {col}: {pd_values.quantile(0.5, interpolation='higher')},"+
    f"mean: {pd_values.mean().round(2)}")
    print(f"{values_quantiles}")
    plt.figure(figure)
    texts_plot = pdtl_percentiles.plot(**plot_kwargs)
    return texts_plot, pd_values



# %%



for col, linestyle in [
    ("nb_from_dhs", linestyle_from_dhs),
    ("nb_to_dhs", linestyle_from_ef_to_dhs),
]:
    for lng in languages:
        links_per_article_distribution_plot, values = links_stats_distribution(
            links_stats_per_article[lng],
            col,"Whole HDS",37,
            color=colors_by_language[lng], linestyle=linestyle, zorder=3
        )
links_per_article_distribution_plot.legend(
    ["Original HDS links "+lng.upper() for lng in languages] + \
    ["HDS Links from entity-fishing "+lng.upper() for lng in languages]
)
links_per_article_distribution_plot.set(
    title= "Distribution of articles according to number of HDS links",
    ylabel="# of links",
    xlabel= "Articles (percentiles by number of links)"
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)

plt.show()
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_hds_ef_links_per_article_distribution_figure, dpi=500)




# %%
for col, linestyle in [
    ("nb_from_dhs_per_nb_char", linestyle_from_dhs),
    ("nb_to_dhs_per_nb_char", linestyle_from_ef_to_dhs),
    ("nb_to_dhs_wd_per_nb_char", linestyle_from_ef_to_all)
]:
    for lng in languages:
        links_per_article_distribution_plot, values = links_stats_distribution(
            links_stats_per_article[lng],
            col, "Whole HDS",38,
            color=colors_by_language[lng], linestyle=linestyle, zorder=3
        )
links_per_article_distribution_plot.legend(
    ["Original HDS links "+lng.upper() for lng in languages] + \
    ["HDS Links from entity-fishing "+lng.upper() for lng in languages] + \
    ["All Links from entity-fishing "+lng.upper() for lng in languages]
)
links_per_article_distribution_plot.set(
    title= "Distribution of articles according to number of HDS links per 1000 character",
    ylabel="# of links per 1000 characters",
    xlabel= "Articles (percentiles by number of links per 1000 characters)"
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_hds_ef_links_per_article_distribution_breakdown_figure, dpi=500)

# %%


links_stats_per_article["fr"][links_stats_per_article["fr"].nb_from_dhs>100]
# %%














# %%

print("DONE")

# %%

# %%

"""
SCP COPY FIGURES:
scp -r ddupertu@128.178.21.4:/home/ddupertu/Documents/dhs-nerd/reports/figures .
"""
