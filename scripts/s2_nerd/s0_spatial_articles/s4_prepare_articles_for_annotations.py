
# %%

import json
import re
from warnings import warn

from cassis import *

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from polities_to_extract_rules import *
from data_file_paths import *

# %%


language="fr"

articles = get_articles(language)
articles_by_category = get_articles_by_category(articles)
spatial_articles = articles_by_category["spatial"]

polities = get_polities_to_extract(spatial_articles=spatial_articles)
polities_dtf = get_polities_to_extract_dtf(polities)
polities_dtf.head()

# %%


polities_dtf["original_title"] = polities_dtf.title

def get_titles_containing_str(s, title_column="original_title"):
    return polities_dtf[polities_dtf[title_column].apply(lambda t: s in t)]

def get_terms_from_title(t):
    return [w.replace(",","") for w in t.replace("L' ", "L'").replace("d' ", "d'").split(" ")]

pd.set_option('display.max_rows', None)
# analysis of terms in polities titles
polities_dtf["terms"] = polities_dtf.title.apply(get_terms_from_title)

titles_terms = [w for t in polities_dtf.terms for w in t]
titles_terms[0:5]

terms_stats = pd.Series(titles_terms).value_counts()
terms_stats [0:50]
# %%

# -> are there terms having upper case letters in the middle?
# (badly fusioned title words seen once or thwice somewhere)
maj_in_middle_regex = re.compile(r".+\w[A-Z]")
maj_in_middle_all = [maj_in_middle_regex.search(w)for w in terms_stats.index]
maj_in_middle = [w for w in maj_in_middle_all if w is not None]
maj_in_middle
len(maj_in_middle)
# -> no! only cantons initials...

# %%

terms_stats_dtf = terms_stats.to_frame("term_count")
terms_stats_dtf["term"] = terms_stats_dtf.index
terms_stats_dtf
# %%
terms_stats_dtf[terms_stats_dtf.term_count>1]

terms_stats_dtf.to_csv(s2_hds_article_titles_terms_csv, index=False)
terms_stats_dtf.head(20)
# %%
"""things to correct in titles:
- remove ,

questions:
- what to do with cantonal affiliation?
    -> generally used for homonyms
- what to do with "/" ?
    -> indicate multilingual titles (Albula/Alvra...), mainly GR
"""

# %%

unwanted_chars_regex = re.compile(r",|\(|\)|/")
only_upper_case_regex = re.compile(r"^[A-Z]+$")
unwanted_terms_dtf = terms_stats_dtf[terms_stats_dtf.term.apply(lambda t: unwanted_chars_regex.search(t) is not None or only_upper_case_regex.match(t) is not None)]
unwanted_terms_dtf.shape

# %%

# are terms without a starting upper case enough to identify unwanted words?

terms_without_upper_case_start = terms_stats_dtf[terms_stats_dtf.term.apply(lambda t: t[0] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")]
# -> yes it works pretty good!
"""
Special treatments:
- "d' " -> remove the space
- "Einsiedeln abbaye de bénédictins"
    -> "de" is not part of stopwords
    -> how to remove?
- Milan duché
    -> useful information as it is not mentioned in the dhstag
"""

terms_without_upper_case_start.to_csv(s2_hds_article_titles_terms_to_remove_csv, index=False)

terms_without_upper_case_start
# %%

terms_to_remove = pd.read_csv(s2_hds_article_titles_terms_to_remove_hand_corrected_csv)

# %%

get_titles_containing_str("département")

# %%



polities_dtf[polities_dtf.terms.apply(lambda t: "d'Otmarsberg" in t)]

# %%
polities_dtf[polities_dtf.title.apply(lambda t: "commune" in t)].shape


# %%

"""
Strategy to correct entity-names to identify proper status-words and obtain canonic title:
- detect all statuswords
    -> list of statuswords
    -> what about composed statuswords (principauté abbatial, chapitre collégial):
        011604 Einsiedeln (abbaye de bénédictines)
        011491 Einsiedeln (abbaye de bénédictins)
        008394 Saint-Gall (principauté abbatiale)
        012120 Saint-Ursanne (chapitre collégial)
- keep the one consistent with entity-tag
    -> list of statusword with corresponding entity-tag
-

notes:
- 012128 institut de Menzingen, fondé en 1844
    -> pas relevant car n'a jamais contrôlé de territoire
- 012991 Uznach - abbaye d'Otmarsberg, fondé ~1919
    -> pas relevant

titles that I do want to obtain:
- original title: original title as obtained from HDS
- canonic_title: unambiguous name for an entity
- alternative_titles: possible other titles (with/without status word or cantonal affiliation)

todo:
- adding missing entities based on names (dizain, pieve)
- abbaye-couvent-monastère-prieuré default tag name is whut?
- évêché-état disparu doublons
"""

terms_without_upper_case_start.to_csv(s2_hds_article_titles_statuswords_csv, index=False)

status_words_dtf = pd.read_csv(s2_hds_article_titles_statuswords_hand_corrected_csv)
status_words_dtf["tags"] = status_words_dtf.term.apply(lambda t: [])
status_words_dtf.to_json(s2_hds_article_titles_statuswords_json, indent=2, orient="records", force_ascii=False)
status_words_dtf = pd.read_json(s2_hds_article_titles_statuswords_hand_corrected_json)

status_words_dict = {
    r[1]["term"]: r[1]["tags"]
    for r in status_words_dtf.iterrows()
}

# %%

terms_to_remove[terms_to_remove.term.apply(lambda t: t not in set(status_words_dtf.term))]
# -> only 5 terms to remove that aren't status words, and only 1 (chateau) linked to polities that doesnt need hand correction anyway


# %%

status_words_set = set(status_words_dtf.term)
polities_with_status = polities_dtf[polities_dtf.terms.apply(lambda ts: sum(t in status_words_set for t in ts)>=1)]
polities_with_status["status_words"] = polities_with_status.terms.apply(lambda ts: frozenset([t for t in ts if t in status_words_set]))
polities_with_status["nb_status_words"] = polities_with_status.status_words.apply(len)

len(set(polities_with_status.status_words))

"""
frozenset({'bailliage', 'commanderie'})
 frozenset({'diocèse', 'évêché'}),
 frozenset({'bailliage', 'district', 'pieve'}),
 frozenset({'bailliage', 'comté'}),
 frozenset({'couvent', 'district'}),
 frozenset({'bailliage', 'seigneurie'})}

only problematic one is frozenset({'diocèse', 'évêché'}),
-> concerns 2 articles, Genève and Coire
"""

polities_with_status[polities_with_status["status_words"].apply(lambda sw: sw==frozenset({'diocèse', 'évêché'}))]

# %%

with open(s2_hds_tag_default_status_word) as f:
    tags_default_status_words = json.load(f)

# %%

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

def get_title_components(pid, original_title, tagname, status_words_dict, tags_default_status_words=tags_default_status_words):
    """returns a 4-tuple containing: canonic title, typology, toponym, geo-identifier
    
    - canonic title: unique title containing the three following component of the tuple
    - typology: (optional) abbaye/commune/seigneurie/..., None if not present
    - toponym: name of the place to which the entity refers
    - geoidentifier: (optional) if the toponym has homonyms serves as unique identifier, None if not present
    
    """
    geoidentifier=get_geoidentifier(original_title, status_words_dict)
    terms = [remove_parentheses(t) for t in get_terms_from_title(original_title)]

    status_words = [t for t in terms if t in status_words_dict]
    non_status_words = [t for t in terms if t not in status_words_dict and t != geoidentifier]
    relevant_status_words = [sw for sw in status_words if tagname in status_words_dict[sw]]
    toponym = " ".join(non_status_words)
    if len(status_words)==0:
        return (original_title, None, original_title, geoidentifier)
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
        warn(f"get_canonic_title() for entity {pid} - {original_title} has multiple relevant status words: {relevant_status_words}")
    return ("PROBLEM", "PROBLEM", "PROBLEM", "PROBLEM")

def get_dtf_titles_components(dtf, status_words_dict):
    title_components = [get_title_components(r["polity_id"], r["original_title"], r["dhstag"].tag, status_words_dict) for i, r in dtf.iterrows()]
    dtf["canonic_title"] = [tc[0] for tc in title_components] 
    dtf["typology"] = [tc[1] for tc in title_components] 
    dtf["toponym"] = [tc[2] for tc in title_components] 
    dtf["geoidentifier"] = [tc[3] for tc in title_components] 

def get_canonic_title(pid, original_title, tagname, status_words_dict, tags_default_status_words=tags_default_status_words):
    """
    algorithm:
    - detect sw and non-sw
    - identify pertinent sw
    - keep only pertinent sw with added "xxx de yyy"
    """
    terms = get_terms_from_title(original_title)

    status_words = [t for t in terms if t in status_words_dict]
    non_status_words = [t for t in terms if t not in status_words_dict]
    relevant_status_words = [sw for sw in status_words if tagname in status_words_dict[sw]]
    if len(status_words)==0:
        return original_title
    elif len(relevant_status_words)==0:
        if tags_default_status_words[tagname] is not None:
            return " ".join([tags_default_status_words[tagname],"de"]+non_status_words)
        else:
            return " ".join(non_status_words)
    elif len(relevant_status_words)==1:
        return " ".join([relevant_status_words[0],"de"]+non_status_words)
    elif len(relevant_status_words)>1:
        warn(f"get_canonic_title() for entity {pid} - {original_title} has multiple relevant status words: {relevant_status_words}")
    return "PROBLEM"

def get_dtf_canonic_titles(dtf, status_words_dict):
    dtf["canonic_title"] = [get_canonic_title(r["polity_id"], r["original_title"], r["dhstag"].tag, status_words_dict) for i, r in dtf.iterrows()]


# %%

get_dtf_canonic_titles(polities_dtf, status_words_dict)#["canonic_title"] = [get_canonic_title(r["polity_id"], r["original_title"], r["dhstag"].tag, status_words_dict) for i, r in polities_dtf.iterrows()]
# %%

# %%

get_dtf_canonic_titles(polities_with_status, status_words_dict)
# %%
polities_with_status[["polity_id", "original_title", "canonic_title", "dhstag"]]

# %%

get_titles_containing_str("PROBLEM", "canonic_title")
get_titles_containing_str("Genève", "canonic_title")

# %%
get_titles_containing_str("château", "canonic_title")
# %%

get_dtf_titles_components(polities_dtf, status_words_dict)
polities_dtf[["polity_id", "original_title", "canonic_title", "typology", "toponym", "geoidentifier", "dhstag"]][0:50]

# %%
