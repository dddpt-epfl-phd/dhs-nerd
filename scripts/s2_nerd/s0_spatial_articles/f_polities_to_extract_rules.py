

import json
import re
from warnings import warn

import pandas as pd

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from data_file_paths import *

from Polity import *


custom_hds_tag = DhsTag("Custom", "u=99999")

def get_articles(language="fr"):
    articles_jsonl_file = localize(S0_JSONL_ALL_ARTICLES_PARSED_FILE, language)
    articles = list(DhsArticle.load_articles_from_jsonl(articles_jsonl_file))
    return articles

def get_articles_by_category(articles):
    language="fr" # categories are the same in all languages, they have been scraped in fr only
    empty_articles_by_category = {c:set(DhsArticle.load_articles_from_jsonl(localize(f, language))) for c,f in S0_JSONL_ARTICLES_BY_CATEGORIES_FILES.items()}
    articles_ids_by_category = {c:set(a.id for a in abc) for c,abc in empty_articles_by_category.items()}
    articles_by_category = {
        c:set([a for a in articles if a.id in abyc])
        for c,abyc in articles_ids_by_category.items()
    }
    return articles_by_category


with open(s2_hds_tagname_to_initial) as f:
    tagname_to_initial = json.load(f)
def get_initial_from_tag(tag):
    return tagname_to_initial[tag] if tag in tagname_to_initial else tagname_to_initial["other"]

def tag_name_to_short_name(n):
    return n.split("/")[-1].strip()

def get_polities_tags_extraction_rules_hand_filled(**kwargs):
    """Returns a dataframe containing the polities tags extraction rules filled by hand
    
    Does some dumb preprocessing (columns ordering, replacing NaNs)
    """
    tags_to_extract = pd.read_csv(s2_s1_polities_tags_extraction_rules_hand_filled)
    tags_to_extract = tags_to_extract.loc[~tags_to_extract.depth.isna()]
    tags_to_extract.nb_articles[tags_to_extract.nb_articles.isna()] = 0
    tags_to_extract["hds_tag"] = tags_to_extract.name.apply(lambda n: DhsTag(n))
    tags_to_extract["short_name"] = tags_to_extract.name.apply(tag_name_to_short_name)
    tags_to_extract_reordered_columns = set(["depth", "name", "short_name"])
    tags_to_extract = tags_to_extract[["depth", "short_name"] + [c for c in tags_to_extract.columns if c not in tags_to_extract_reordered_columns] +["name"]]
    return tags_to_extract

def get_selected_tags_dtf(tags_extraction_rules=None, **kwargs):
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
    return set(selected_tags_dtf["hds_tag"])

title_terms_indicating_extra_polity = list(pd.read_csv(s2_hds_title_terms_indicating_extra_polity).term)
def add_extra_polities_from_articles_title(selected_articles):
    selected_articles = [
        (a, atags+[custom_hds_tag], nbtags+1)
        if any(t in a.title for t in title_terms_indicating_extra_polity)
        else (a, atags, nbtags)
        for a, atags, nbtags in selected_articles
    ]
    return selected_articles

def handle_eveche_exception(selected_articles):
    """The "Eveche, Diocèse" tag is really a polity only if it is accompanied by the "Etat historique disparu" tag

    Hence this function
    - removes "Eveche, Diocèse" if it is not accompanied by etat historique disparu
    - removes "Etat historique disparu" tag from accompanied "Eveche, Diocèse" tags
    Entités politiques / Etat historique disparu
    Entités ecclésiastiques / Evêché, diocèse
    """
    ev_tag = DhsTag("Entités ecclésiastiques / Evêché, diocèse")
    ehd_tag = DhsTag("Entités politiques / Etat historique disparu")
    def correct_eveche_tags(article, tags, nbtags):
        if ev_tag not in tags:
            return (article, tags, nbtags)
        elif ehd_tag in tags:
            return (article, [t for t in tags if t!=ehd_tag], nbtags-1)
        else :
            return (article, [t for t in tags if t!=ev_tag], nbtags-1)
    return [
        correct_eveche_tags(a, atags, nbtags)
        for a, atags, nbtags in selected_articles
    ]

unwanted_hds_ids= set([
    "012128", # institut de Menzingen, fondé en 1844, pas pertinent car n'a jamais contrôlé de territoire
    "012991" # Uznach - abbaye d'Otmarsberg, fondé ~1919, pas pertinent
])
unwanted_hds_ids_tags={
    "008394": [DhsTag("Entités politiques / Etat historique disparu")] # principauté abbatiale de Saint-Gall
}
def selected_articles_post_correction(selected_articles):
    selected_articles = [
        (a, atags, nbtags)
        for a, atags, nbtags in selected_articles
        if a.id not in unwanted_hds_ids
    ]
    selected_articles = [
        (a, atags, nbtags)
        if a.id not in unwanted_hds_ids_tags
        else (
            a,
            [t for t in atags if t not in unwanted_hds_ids_tags[a.id]],
            nbtags-len(unwanted_hds_ids_tags[a.id])
        )
        for a, atags, nbtags in selected_articles
    ]
    return selected_articles

def get_selected_articles(spatial_articles, selected_tags=None, **kwargs):
    """Returns a list of tuples each containing: a selected article, its selected tags, the nb of selected tags
    
    A polity should be created for each article-tag pair of the resulting list
    """
    if selected_tags is None:
        selected_tags = get_selected_tags(**kwargs)
    selected_articles = [(a,[t for t in a.tags if t in selected_tags]) for a in spatial_articles]
    selected_articles = [(a, atags,len(atags)) for a, atags in selected_articles if len(atags)>0]
    selected_articles = add_extra_polities_from_articles_title(selected_articles)
    selected_articles = handle_eveche_exception(selected_articles)
    selected_articles = selected_articles_post_correction(selected_articles)
    return selected_articles

def get_polities_to_extract(selected_articles=None, **kwargs):
    """Returns a list with 1 tuple per polity
    
    A tuple contains: the unique polity id, the corresponding article and tag as well as the total nb of selected tags of the article"""
    if selected_articles is None:
        selected_articles = get_selected_articles(**kwargs)
    polities = [
        (a.id+"-"+get_initial_from_tag(t.tag), a, t, nbtags)
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
    ], columns=["polity_id", "article_title", "hds_tag", "nbtags", "hds_id"])
    # merging in level info
    polities_dtf["name"] = polities_dtf.hds_tag.apply(lambda t: t.tag)
    polities_dtf = polities_dtf.merge(selected_tags_dtf[["name","level"]], on="name")
    polities_dtf.drop("name", axis=1, inplace=True)
    return polities_dtf





with open(s2_hds_tag_default_status_word) as f:
    tags_default_status_words = json.load(f)

def get_terms_from_title(t):
    return [w.replace(",","") for w in t.replace("L' ", "L'").replace("d' ", "d'").split(" ")]

def remove_parentheses(t):
    return t.replace("(", "").replace(")", "")

parentheses_chars_regex = re.compile(r"\(|\)")
only_upper_case_regex = re.compile(r"^[A-Z]+$")
def get_geoidentifier(title, status_words_dict):
    """Extracts the geoidentifier (if present) from a polity's title
    
    strategy:
    - get all terms with ( or )
    - get all terms with capitals only
    - check that term aren't status words
    """
    terms = get_terms_from_title(title)

    geoidentifier_terms = [t for t in terms if parentheses_chars_regex.search(t) is not None or only_upper_case_regex.match(t) is not None]
    geoidentifier_terms = [remove_parentheses(t) for t in geoidentifier_terms]
    geoidentifier_terms = [t for t in geoidentifier_terms if t not in status_words_dict]
    if len(geoidentifier_terms)==0:
        return None
    else:
        return " ".join(geoidentifier_terms)


def get_canonic_title_from_components(typology, toponym, geoidentifier):
    return typology+" de "+toponym + (" ("+geoidentifier+")" if geoidentifier is not None else "")


hand_corrected_titles = {
    "011604-m": ("abbaye de bénédictines", "Einsiedeln",None),
    "011491-m": ("abbaye de bénédictins", "Einsiedeln",None),
    "008394-m": ("principauté abbatiale", "Saint-Gall",None),
    "012120-cclg": ("chapitre collégial", "Saint-Ursanne",None)
}
def titles_post_correction(polity_id, title_components):
    if polity_id in hand_corrected_titles:
        return (get_canonic_title_from_components(*hand_corrected_titles[polity_id]), *hand_corrected_titles[polity_id])
    else:
        return title_components


def get_title_components(pid, article_title, tagname, status_words_dict, tags_default_status_words=tags_default_status_words):
    """returns a 4-tuple containing: canonic title, typology, toponym, geo-identifier
    
    - canonic title: unique title containing the three following component of the tuple
    - typology: (optional) abbaye/commune/seigneurie/..., None if not present
    - toponym: name of the place to which the entity refers
    - geoidentifier: (optional) if the toponym has homonyms serves as unique identifier, None if not present
    
    """
    geoidentifier=get_geoidentifier(article_title, status_words_dict)
    terms = [remove_parentheses(t) for t in get_terms_from_title(article_title)]

    status_words = [t for t in terms if t in status_words_dict]
    non_status_words = [t for t in terms if t not in status_words_dict and t != geoidentifier]
    relevant_status_words = [sw for sw in status_words if tagname in status_words_dict[sw]]
    toponym = " ".join(non_status_words)
    if len(status_words)==0:
        return (article_title, None, article_title, geoidentifier)
    elif len(relevant_status_words)==0:
        typology = tags_default_status_words[tagname]
        if typology is not None:
            canonic_title = get_canonic_title_from_components(typology, toponym, geoidentifier)
            return (canonic_title, typology, toponym, geoidentifier)
        else:
            return (toponym, None, toponym, geoidentifier)
    elif len(relevant_status_words)==1:
        typology = relevant_status_words[0]
        canonic_title = get_canonic_title_from_components(typology, toponym, geoidentifier)
        return (canonic_title, typology, toponym, geoidentifier)
    elif len(relevant_status_words)>1:
        warn(f"get_canonic_title() for entity {pid} - {article_title} has multiple relevant status words: {relevant_status_words}")
    return ("PROBLEM", "PROBLEM", "PROBLEM", "PROBLEM")


def get_dtf_titles_components(dtf, status_words_dict):
    title_components = [titles_post_correction(
        r["polity_id"],
        get_title_components(r["polity_id"], r["article_title"], r["hds_tag"].tag, status_words_dict))
        for i, r in dtf.iterrows()
    ]
    dtf["canonic_title"] = [tc[0] for tc in title_components] 
    dtf["typology"] = [tc[1] for tc in title_components] 
    dtf["toponym"] = [tc[2] for tc in title_components] 
    dtf["geoidentifier"] = [tc[3] for tc in title_components] 

def from_dtf_polity_list(dtf):
    """unimplemented: get a csv out"""
    if False:
        def create_polity(r):
            print(r["geoidentifier"])
            Polity(r["polity_id"], r["toponym"], r["typology"], r["geoidentifer"], r["hds_tag"], r["hds_id"])
        polities = [
            create_polity(r)
            for i,r in dtf.iterrows()
        ]
        return polities
        #Polity(polity_id, toponym, typology=None, geoidentifer=None, hds_tag=None, hds_article_id=None)