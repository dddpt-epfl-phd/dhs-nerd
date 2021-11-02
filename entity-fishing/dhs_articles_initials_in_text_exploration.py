# %%
from random import sample, seed
import re

import pandas as pd
from webbrowser import open as op

from dhs_scraper import DhsArticle
from utils import get_dhs_dump_jsonl_file, CATEGORIES
from dhs_articles_initials_in_text import get_article_identifying_initial

seed(54367)

# %%

explored_languages=["fr", "de"]
lng="fr"

# %%

all_ids = list(DhsArticle.get_articles_ids(get_dhs_dump_jsonl_file(lng)))
sampled_ids = sample(all_ids, 1000)

# %%

articles = list(DhsArticle.load_articles_from_jsonl(get_dhs_dump_jsonl_file(lng)))#, sampled_ids))


# %%

initial_regex = re.compile(r" ([A-Z])\.\W")

min_title_element_length = 2
def get_title_initials(title):
    initials = set(s[0] for s in title.split(" ") if len(s)>=min_title_element_length)
    if len(initials)>0:
        return initials
    else:
        return set(s[0] for s in title.split(" "))

initials = [
    (
        a,
        pd.Series(initial_regex.findall(a.text)).value_counts(),
        set(s[0] for s in a.title.split(" ") if s[0].isupper())
    ) for a in articles
]
missing_title_initials = [ i for i in initials if len(i[2])==0]
if len(missing_title_initials)>0:
    print(f"SOME ARTICLES HAVE NO TITLE INITIALS:\n{missing_title_initials}")

# %%

initials_nb = [len(i[1]) for i in initials]
initials_nb_distrib = pd.Series(initials_nb).value_counts()
# only ~10% articles have more than 1 initial...
initials_nb_distrib

# %%


one_initial = [i  for i in initials if len(i[1])==1]

one_initial_orphelins = [(a,i,it) for a,i,it in one_initial if i.index[0] not in it]
# -> 1 initial that isn't in title initials: artifact, not valid

no_initials = [i  for i in initials if len(i[1])==0]
# -> mostly short articles about people/families

# %%

multiple_initials = [i for i in initials if len(i[1])>1]
multiple_initials

two_most_likely_initials_occurence_diff = [i[0]-i[1] for a, i, it in multiple_initials]
pd.Series(two_most_likely_initials_occurence_diff).value_counts()

# %%

first_most_likely_initial_in_title_initials = [(i.index[0] in it) for a, i, it in multiple_initials if len(i)>0]
pd.Series(first_most_likely_initial_in_title_initials).value_counts()
# %%

second_most_likely_initial_in_title_initials = [(i.index[1] in it) for a, i, it in multiple_initials if len(i)>0]
pd.Series(second_most_likely_initial_in_title_initials).value_counts()

# %%

two_most_likely_initial_in_title_initials = [
    (i.index[0] in it) and
    (i.index[1] in it)
    for a, i, it in multiple_initials if len(i)>0
]
pd.Series(two_most_likely_initial_in_title_initials).value_counts()
# %%

only_second_most_likely_initial_in_title_initials = [
    (not i.index[0] in it) and
    (i.index[1] in it)
    for a, i, it in multiple_initials if len(i)>0
]
pd.Series(only_second_most_likely_initial_in_title_initials).value_counts()
# %%

two_most_likely_initial_not_in_title_initials = [
    (not i.index[0] in it) and
    (not i.index[1] in it)
    for a, i, it in multiple_initials if len(i)>0
]
pd.Series(two_most_likely_initial_not_in_title_initials).value_counts()

# %%
def slice_from_truth_list(l, tl):
    return [l[i] for i,tv in enumerate(tl) if tv]


pd.Series(slice_from_truth_list(two_most_likely_initials_occurence_diff, only_second_most_likely_initial_in_title_initials)).value_counts()

# %%

only_second = slice_from_truth_list(multiple_initials, only_second_most_likely_initial_in_title_initials)
op(only_second[56][0].url)
# -> in this case, second is the right choice!

two_most = slice_from_truth_list(multiple_initials, two_most_likely_initial_in_title_initials)
op(two_most[43][0].url)
two_most[21][1] # -> "Rodolphe Louis de Goumoëns" is a challenging example: L. and G. appear in text, only second is right -> take last title initial
# -> people with first name last name at equal mentions: last name is used by DHS as abbreviation, first name is in text as companies name

# %%

articles_ids_by_category = [(c, set(DhsArticle.get_articles_ids(p))) for c,p in CATEGORIES]

print("categories of articles with two most likely text initials in title:")
for c, ids in articles_ids_by_category:
    arts = [a for a,i ,it in two_most if a.id in ids]
    print(f"{c}: {len(arts)}")
    if c=="families":
        print([a.url for a in arts])
# -> validates the theory that two_most are always people with first name used in companies names.
print("------")
print("categories of articles with only second most likely text initials in title:")
for c, ids in articles_ids_by_category:
    print(f"{c}: {len([a for a,i ,it in only_second if a.id in ids])}")


# %%

# checking out the get_article_identifying_initial() method

identifying_initial = [(a,i,it,get_article_identifying_initial(a)) for a,i,it in initials]
# %%
sum(ii is not None for a,i,it,ii in identifying_initial) # fr:29906, de: 27332
sum(ii in i.index for a,i,it,ii in identifying_initial) # fr:29906
sum(ii in it for a,i,it,ii in identifying_initial) # fr:29906
len(no_initials) # fr: 6016, de: 8486
len(one_initial_orphelins) # fr: 397, de:462
sum(two_most_likely_initial_not_in_title_initials) # fr: 36, de 76
sum(ii is not None for a,i,it,ii in identifying_initial)+len(no_initials)+len(one_initial_orphelins)+sum(two_most_likely_initial_not_in_title_initials) # fr: 29906+6016+397+36 = 36355
# %%
