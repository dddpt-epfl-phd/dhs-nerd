
# %%

import re

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

def get_titles_containing_str(s):
    return polities_dtf[polities_dtf.original_title.apply(lambda t: s in t)]

pd.set_option('display.max_rows', None)
# analysis of terms in polities titles
titles = list(polities_dtf.title)

titles_terms = [w.replace(",","") for t in titles for w in t.split(" ")]
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
- remove (...)
- remove cantonal affiliation (VD), (ZH), etc...

questions:
- what to do with cantonal affiliation?
    -> generally used for homonyms
- what to do with "/" ?
    -> indicate multilingual titles (Albula/Alvra...), mainly GR
"""

# %%

unwanted_chars_regex = re.compile(",|\(|\)|/")
terms_stats_dtf[terms_stats_dtf.term.apply(lambda t: unwanted_chars_regex.search(t) is not None)]


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

get_titles_containing_str("duché")

# %%

