# %%


import sys

from typing import Sequence

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

lng_names={
    "fr": "French",
    "de": "German",
    "it": "Italian"
}

# %%


def articles_text_links_stats(articles:Sequence[DhsArticle]):
    articles_stats = []
    articles_linking_to_stats = {
        a.id: {
            "from_dhs": set(),
            "from_ef": set(),
        }
        for a in articles
    }
    for article in articles:
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
                    if dhsid is not None and dhsid in articles_linking_to_stats:
                        articles_linking_to_stats[dhsid]["from_dhs"].add(article.id)
                elif origin==ORIGIN_FROM_ENTITY_FISHING:
                    wd_url = get_wikidata_url(tl)
                    wk_page = get_wikipedia_page_id(tl)
                    from_ef.add(wd_url)    
                    if dhsid is not None:
                        to_dhs.add(dhsid)
                        if dhsid in articles_linking_to_stats:
                            articles_linking_to_stats[dhsid]["from_ef"].add(article.id)
                    elif wd_url is not None:
                        to_wd.add(wd_url)
                    elif wk_page is not None:
                        to_wk.add(wk_page)
                    else:
                        nb_unlinked+=1
        articles_stats.append({
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
        })
    for a in articles_stats:
        a["nb_linking_to_from_dhs"] = len(articles_linking_to_stats[a["dhsid"]]["from_dhs"])
        a["nb_linking_to_from_ef"] = len(articles_linking_to_stats[a["dhsid"]]["from_ef"])
    return pd.DataFrame(articles_stats)


# %%

print("computing links statistics...")
links_stats_per_article = {
    lng: articles_text_links_stats(linked_articles[lng])
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
    title = "Figure 2: Number of HDS articles whose last version is in year",
    xlabel="Year of latest version",
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
    xlabel="Year of latest version",
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
    title = "Figure 3: Number of links per 1000 characters per year in the HDS",
    xlabel="Year of latest version",
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
    xlabel="Year of latest version",
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
links_per_a_distrib_languages = ["fr", "de"]
links_per_article_distribution_values_by_col_lng = dict()
for col, linestyle in [
    ("nb_from_dhs_per_nb_char", linestyle_from_dhs),
    ("nb_to_dhs_per_nb_char", linestyle_from_ef_to_dhs),
    ("nb_to_dhs_wd_per_nb_char", linestyle_from_ef_to_all)
]:
    links_per_article_distribution_values_by_col_lng[col] = dict()
    for lng in links_per_a_distrib_languages:
        links_per_article_distribution_plot, values = links_stats_distribution(
            links_stats_per_article[lng],
            col, "Whole HDS",38,
            color=colors_by_language[lng], linestyle=linestyle, zorder=3
        )
        links_per_article_distribution_values_by_col_lng[col][lng] = values
ladvcl = links_per_article_distribution_values_by_col_lng
links_per_article_distribution_plot.legend(
    ["Original HDS links "+lng.upper() for lng in links_per_a_distrib_languages] + \
    ["HDS Links from entity-fishing "+lng.upper() for lng in links_per_a_distrib_languages] + \
    ["All Links from entity-fishing "+lng.upper() for lng in links_per_a_distrib_languages]
)
links_per_article_distribution_plot.set(
    title= "Figure 5: Distribution of articles according to number of HDS links per 1000 characters",
    ylabel="# of links per 1000 characters",
    xlabel= "Articles (percentiles by number of links per 1000 characters)"
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_hds_ef_links_per_article_distribution_breakdown_figure, dpi=500)

print("Article median and avg for 'number of HDS links per 1000 characters':\n- " + ("\n- ".join(
    ["Original HDS links "+lng.upper()+f", median: {round(ladvcl['nb_from_dhs_per_nb_char'][lng].median(),2)}, avg: {round(ladvcl['nb_from_dhs_per_nb_char'][lng].mean(),2)}" for lng in links_per_a_distrib_languages] + \
    ["HDS Links from entity-fishing "+lng.upper()+f", median: {round(ladvcl['nb_to_dhs_per_nb_char'][lng].median(),2)}, avg: {round(ladvcl['nb_from_dhs_per_nb_char'][lng].mean(),2)}" for lng in links_per_a_distrib_languages] + \
    ["All Links from entity-fishing "+lng.upper()+f", median: {round(ladvcl['nb_to_dhs_wd_per_nb_char'][lng].median(),2)}, avg: {round(ladvcl['nb_from_dhs_per_nb_char'][lng].mean(),2)}" for lng in links_per_a_distrib_languages]
)))

# %%


links_stats_per_article["fr"][links_stats_per_article["fr"].nb_from_dhs>100]
# %%






# %%
nb_linking_to_article_distribution_values_by_col_lng = dict()
for col, linestyle in [
    ("nb_linking_to_from_dhs", linestyle_from_dhs),
    ("nb_linking_to_from_ef", linestyle_from_ef_to_dhs),
]:
    nb_linking_to_article_distribution_values_by_col_lng[col] = dict()
    for lng in languages:
        nb_linking_to_article_distribution_plot, values = links_stats_distribution(
            links_stats_per_article[lng],
            col, f"Whole {lng} HDS",469,
            color=colors_by_language[lng], linestyle=linestyle, zorder=3
        )
        nb_linking_to_article_distribution_values_by_col_lng[col][lng] = values
ladvcl = nb_linking_to_article_distribution_values_by_col_lng
nb_linking_to_article_distribution_plot.legend(
    ["Original HDS links "+lng.upper() for lng in languages] + \
    ["HDS Links from entity-fishing "+lng.upper() for lng in languages] + \
    ["All Links from entity-fishing "+lng.upper() for lng in languages]
)
nb_linking_to_article_distribution_plot.set(
    title= "Distribution of articles according to number of other HDS articles linking to article",
    ylabel="# of other articles linking to article",
    xlabel= "Articles (percentiles by number of other articles linking to article)"
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)
plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_hds_ef_nb_linking_to_article_distribution_breakdown_figure, dpi=500)

print("Article median and avg for 'number of other HDS articles linking to article':\n- " + ("\n- ".join(
    ["Original HDS links "+lng.upper()+f", median: {round(ladvcl['nb_linking_to_from_dhs'][lng].median(),2)}, avg: {round(ladvcl['nb_linking_to_from_dhs'][lng].mean(),2)}" for lng in languages] + \
    ["HDS Links from entity-fishing "+lng.upper()+f", median: {round(ladvcl['nb_linking_to_from_ef'][lng].median(),2)}, avg: {round(ladvcl['nb_linking_to_from_ef'][lng].mean(),2)}" for lng in languages]
)))


links_stats_per_article["fr"][links_stats_per_article["fr"].nb_linking_to_from_ef>2000].sort_values(by="nb_linking_to_from_ef")








# %%

nb_linking_to_language="fr"
dtf = links_stats_per_article[nb_linking_to_language]
articles_ids_by_category = {c:set(a.id for a in DhsArticle.load_articles_from_jsonl(localize(f, "fr"))) for c,f in S0_JSONL_ARTICLES_BY_CATEGORIES_FILES.items()}
#categories = [c for c in S0_JSONL_ARTICLES_BY_CATEGORIES_FILES.keys()]
# category="themes"

# %%


slng = "fr"
threshold = 1000
top_linked_to = links_stats_per_article[slng][links_stats_per_article[slng].nb_linking_to_from_ef>threshold].sort_values(by="nb_linking_to_from_ef", ascending=False).drop_duplicates()
top_linked_to["EF_nb_linking_to"] = top_linked_to["nb_linking_to_from_ef"]
top_linked_to["Original_HDS_nb_linking_to"] = top_linked_to["nb_linking_to_from_dhs"]
top_linked_to.loc[:,["title", "EF_nb_linking_to", "Original_HDS_nb_linking_to"]].iloc[0:25]

# %%
top_linked_to.loc[:,["title", "EF_nb_linking_to", "Original_HDS_nb_linking_to"]].iloc[25:]

# %%

links_stats_per_article_by_category = {
    category: dtf[dtf.dhsid.apply(lambda x: x in article_ids)]
    for category, article_ids in articles_ids_by_category.items()
}

nb_linking_to_article_distribution_by_col_category_legend = []
for col, linestyle, legend in [
    ("nb_linking_to_from_dhs", linestyle_from_dhs, "Original HDS links to CAT articles"),
    ("nb_linking_to_from_ef", linestyle_from_ef_to_dhs, "Links from entity-fishing to HDS CAT articles"),
]:
    for category, links_stats in list(links_stats_per_article_by_category.items()).__reversed__():
        nb_linking_to_article_distribution_by_col_category_legend.append(legend.replace("CAT",category))
        nb_linking_to_article_distribution_by_category_plot, values = links_stats_distribution(
            links_stats,
            col, legend.replace("CAT",category),321,
            color=colors_by_category[category], linestyle=linestyle, zorder=3
        )

nb_linking_to_article_distribution_by_category_plot.legend(
    nb_linking_to_article_distribution_by_col_category_legend,
    loc='center left'
    #[f"Original HDS links to {category} articles" for category in articles_ids_by_category.keys()] + \
    #[f"Links from entity-fishing to {category} articles" for category in articles_ids_by_category.keys()] 
)
nb_linking_to_article_distribution_by_category_plot.set(
    title= f"Figure 7: Distribution of articles according to number of other\nHDS articles linking to article, by category ({lng_names[nb_linking_to_language]})",
    ylabel="# of other articles linking to article",
    xlabel= "Articles (percentiles by number of other articles linking to article)",
    ylim=(0,1200)
)
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)

nb_linking_to_article_distribution_by_category_plot.text(
    48, 1100,
    f'themes max. nb of articles links to: {"{:,}".format(8172)}c'.replace(",","'"),
    style='italic', color=colors_by_category["themes"], fontsize=9
)
nb_linking_to_article_distribution_by_category_plot.text(
    97.2, 1100, f'=', style='italic',
    color=colors_by_category["themes"], fontsize=12, rotation=30
)
nb_linking_to_article_distribution_by_category_plot.text(
    49, 1030,
    f'spatial max. nb of articles links to: {"{:,}".format(8052)}c'.replace(",","'"),
    style='italic', color=colors_by_category["spatial"], fontsize=9
)
nb_linking_to_article_distribution_by_category_plot.text(
    97.2, 1030, f'=', style='italic',
    color=colors_by_category["spatial"], fontsize=12, rotation=30
)

plt.gcf().set_figwidth(8) # default: 6.4
plt.gcf().set_figheight(5) # default: 4
plt.gcf().savefig(s4_hds_ef_nb_linking_to_article_distribution_by_category_breakdown_figure, dpi=500)

# %%
cat = "themes"
threshold = 1000
links_stats_per_article_by_category[cat][links_stats_per_article_by_category[cat].nb_linking_to_from_ef>threshold].sort_values(by="nb_linking_to_from_ef")


# %%
list(links_stats_per_article_by_category[cat][links_stats_per_article_by_category[cat].nb_linking_to_from_ef>threshold].sort_values(by="nb_linking_to_from_ef").title)
# %%

nb_to_stats = pd.DataFrame([
        (
            c,
            links_stats_per_article["nb_linking_to_from_dhs"].sum(),
            links_stats_per_article["nb_linking_to_from_ef"].sum()
        )
        for c,links_stats_per_article
        in links_stats_per_article_by_category.items()
    ],
    columns=["category", "nb_linking_to_from_dhs", "nb_linking_to_from_ef"]
)
nb_to_stats["nb_linking_to_from_dhs_pct"] = (nb_to_stats["nb_linking_to_from_dhs"] / nb_to_stats["nb_linking_to_from_dhs"].sum() *100).round(2)
nb_to_stats["nb_linking_to_from_ef_pct"] = (nb_to_stats["nb_linking_to_from_ef"] / nb_to_stats["nb_linking_to_from_ef"].sum() *100).round(2)
nb_to_stats


# %%


fig, ax = plt.subplots(figsize=(5,5))

width = 0.3
columns = ["nb_linking_to_from_dhs_pct", "nb_linking_to_from_ef_pct"]
accu = [0]*len(columns)
xlabels = [
    f"Original links from HDS\n({sum(nb_to_stats['nb_linking_to_from_dhs'])} links)",
    f"Links from entity-fishing\n({sum(nb_to_stats['nb_linking_to_from_ef'])} links)"
]

for cat in nb_to_stats["category"]:
    values = [
        float(nb_to_stats[nb_to_stats["category"]==cat][col])
        for col in columns
    ]
    ax.bar(
        xlabels, values,
        bottom=[x for x in accu],
        label=cat,
        width=width, color=colors_by_category[cat],
        zorder=3
    )
    accu = [a+values[i] for i,a in enumerate(accu)]
 
ax.set(
    title=f"Figure 6: Distribution of links according to\n destination article category",
    #+"\n(43% of links from the HDS point to a 'themes' article)",
    ylabel="% of links"
)
#ax.set_xticklabels(xlabels)
ax.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.grid(color = 'lightgrey', linestyle = '--', linewidth = 0.5, zorder=5)
plt.tight_layout()
plt.gcf().savefig(s4_hds_ef_links_to_categories_distribution, dpi=500)
# %%

print("DONE")

# %%

# %%

"""
SCP COPY FIGURES:
scp -r ddupertu@128.178.21.4:/home/ddupertu/Documents/dhs-nerd/reports/figures .
"""
