
# %%

import json
import re
from warnings import warn

from cassis import *

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from f_polities_to_extract_rules import *
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
"""
A title contains up to 3 pieces of information:
- a toponym (Echallens, Zollikofen, etc...)
- (optional) a typology (seigneurie, abbaye, baillage, ...)
- (optional) a geoidentifier (most often cantonal such as VD, GR, sometimes more precise)
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


# %%





# %%

get_dtf_titles_components(polities_dtf, status_words_dict)#["canonic_title"] = [get_canonic_title(r["polity_id"], r["original_title"], r["dhstag"].tag, status_words_dict) for i, r in polities_dtf.iterrows()]
# %%

# %%

get_dtf_titles_components(polities_with_status, status_words_dict)
# %%
polities_with_status[["polity_id", "original_title", "canonic_title", "dhstag"]]

# %%

get_titles_containing_str("PROBLEM", "canonic_title")
get_titles_containing_str("mandement")#, "canonic_title")

# %%
get_titles_containing_str("Ursanne", "canonic_title")
# %%

polities_dtf[["polity_id", "original_title", "canonic_title", "typology", "toponym", "geoidentifier", "dhstag"]][0:50]

# %%

cclg_tag = DhsTag("Entités ecclésiastiques / Chapitre collégial")

polities_dtf[polities_dtf.dhstag.apply(lambda t: t==cclg_tag)]

# %%
