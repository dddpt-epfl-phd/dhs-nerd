
import pandas as pd

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from data_file_paths import s2_s1_polities_tags_extraction_rules_hand_filled

tagname_to_initial = {
    "Entités ecclésiastiques / Abbaye, couvent, monastère, prieuré":"m",
    "Entités ecclésiastiques / Archidiocèse":"ad",
    "Entités ecclésiastiques / Chapitre cathédral":"cc",
    "Entités ecclésiastiques / Commanderie":"cm",
    "Entités ecclésiastiques / Evêché, diocèse":"e",
    "Entités ecclésiastiques / Hospice":"h",
    "Entités politiques / Ancien district":"d",
    "Entités politiques / Ancienne commune":"c",
    "Entités politiques / Bailliage, châtellenie":"b",
    "Entités politiques / Canton":"ct",
    "Entités politiques / Canton, Département, République (1790-1813)":"ct",
    "Entités politiques / Commune":"c",
    "Entités politiques / Comté, landgraviat":"co",
    "Entités politiques / District":"d",
    "Entités politiques / Etat historique disparu":"e",
    "Entités politiques / Seigneurie":"s",
    "Entités politiques / Ville, commune, localité (étranger)":"c"
}

def tag_name_to_short_name(n):
    return n.split("/")[-1].strip()

def get_polities_tags_extraction_rules_hand_filled():
    """Returns a dataframe containing the polities tags extraction rules filled by hand
    
    Does some dumb preprocessing (columns ordering, replacing NaNs)
    """
    tags_to_extract = pd.read_csv(s2_s1_polities_tags_extraction_rules_hand_filled)
    tags_to_extract = tags_to_extract.loc[~tags_to_extract.depth.isna()]
    tags_to_extract.nb_articles[tags_to_extract.nb_articles.isna()] = 0
    tags_to_extract["dhstag"] = tags_to_extract.name.apply(lambda n: DhsTag(n))
    tags_to_extract["short_name"] = tags_to_extract.name.apply(tag_name_to_short_name)
    tags_to_extract_reordered_columns = set(["depth", "name", "short_name"])
    tags_to_extract = tags_to_extract[["depth", "short_name"] + [c for c in tags_to_extract.columns if c not in tags_to_extract_reordered_columns] +["name"]]
    return tags_to_extract

def get_selected_tags_dtf(tags_extraction_rules=None):
    """Returns a dataframe containing only the tags to extract along with a few statistics"""
    if tags_extraction_rules is None:
        tags_extraction_rules = get_polities_tags_extraction_rules_hand_filled()
    selected_tags_dtf = tags_extraction_rules.loc[tags_extraction_rules["polities_extraction_rule"]=="oui"]
    selected_tags_dtf.rename(columns={"nb_articles": "nb_entities"}, inplace=True)
    selected_tags_dtf = selected_tags_dtf.sort_values(["level","nb_entities"],ascending=False)
    selected_tags_dtf["pct_entities"] = selected_tags_dtf.nb_entities / selected_tags_dtf.nb_entities.sum()*100
    return selected_tags_dtf

def get_selected_tags(selected_tags_dtf=None, **kwargs):
    """Returns the set of DhsTags to extract
    
    Note: the DhsTags are incomplete, they only have their tagname, no url or facet"""
    if selected_tags_dtf is None:
        selected_tags_dtf = get_selected_tags_dtf(**kwargs)
    return set(selected_tags_dtf["dhstag"])

def get_selected_articles(spatial_articles, selected_tags=None, **kwargs):
    """Returns a list of tuples each containing: a selected article, its selected tags, the nb of selected tags
    
    A polity should be created for each article-tag pair of the resulting list
    """
    if selected_tags is None:
        selected_tags = get_selected_tags(**kwargs)
    selected_articles = [(a,[t for t in a.tags if t in selected_tags]) for a in spatial_articles]
    selected_articles = [(a, atags,len(atags)) for a, atags in selected_articles if len(atags)>0]
    return selected_articles

def get_polities_to_extract(selected_articles=None, **kwargs):
    """Returns a list with 1 tuple per polity
    
    A tuple contains: the unique polity id, the corresponding article and tag as well as the total nb of selected tags of the article"""
    if selected_articles is None:
        selected_articles = get_selected_articles(**kwargs)
    polities = [
        (a.id+"-"+tagname_to_initial[t.tag], a, t, nbtags)
        for a, tags, nbtags in selected_articles
        for i,t in enumerate(sorted(tags, key=lambda t: t.tag))
    ]
    return polities

def get_polities_to_extract_dtf(polities_to_extract=None,selected_tags_dtf=None, **kwargs):
    """Creates a dtf out of the polities list, adds additional "level" information"""
    if polities_to_extract is None:
        polities_to_extract = get_polities_to_extract(**kwargs)
    if selected_tags_dtf is None:
        selected_tags_dtf = get_selected_tags_dtf(**kwargs)
    polities_dtf = pd.DataFrame([
        (eid, a.title, t, nbtags, a.id)
        for eid, a, t, nbtags in polities_to_extract
    ], columns=["polity_id", "title", "dhstag", "nbtags", "hds_id"])
    # merging in level info
    polities_dtf["name"] = polities_dtf.dhstag.apply(lambda t: t.tag)
    polities_dtf = polities_dtf.merge(selected_tags_dtf[["name","level"]], on="name")
    polities_dtf.drop("name", axis=1, inplace=True)
    return polities_dtf

