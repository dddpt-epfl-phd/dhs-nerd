# %%
from random import sample, seed
import re

import pandas as pd
from webbrowser import open as op

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from dhs_scraper import DhsArticle
from data_file_paths import localize, S0_JSONL_ALL_ARTICLES_FILE, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES

seed(54367)

# %%

explored_languages=["fr", "de"]
lng="de"

# %%

all_ids = list(DhsArticle.get_articles_ids(localize(S0_JSONL_ALL_ARTICLES_FILE, lng)))
sampled_ids = sample(all_ids, 1000)

# %%

print("loading articles...")
articles = list(DhsArticle.load_articles_from_jsonl(localize(S0_JSONL_ALL_ARTICLES_FILE, lng)))#, sampled_ids))
nb_articles = len(set(a.id for a in articles))
print("articles loaded!")

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
        pd.Series(initial_regex.findall(a.text), dtype="U").value_counts(),
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
print(f"Proportion of articles with 1 initial (in title or not): {len(one_initial)/nb_articles}")

one_initial_orphelins = [(a,i,it) for a,i,it in one_initial if i.index[0] not in it]
print(f"Proportion of articles with 1 initial that isn't in title: {len(one_initial_orphelins)/nb_articles}")
# -> 1 initial that isn't in title initials: artifact, not valid

no_initials = [i  for i in initials if len(i[1])==0]
print(f"Proportion of articles without initial: {len(no_initials)/nb_articles}")
# -> mostly short articles about people/families

# %%

multiple_initials = [i for i in initials if len(i[1])>1]
multiple_initials
print(f"Proportion of articles with multiple initials (in title or not): {len(multiple_initials)/nb_articles}")


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

articles_ids_by_category = [(c, set(DhsArticle.get_articles_ids(localize(p, "fr")))) for c,p in S0_JSONL_ARTICLES_BY_CATEGORIES_FILES.items()]

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

print("parsing initials...")
identifying_initial = [(a,i,it,a.initial) for a,i,it in initials]
print("initials parsed!")
# %%
sum(ii is not None for a,i,it,ii in identifying_initial) # fr:29906, de: 27332
sum(ii in i.index for a,i,it,ii in identifying_initial) # fr:29906
sum(ii in it for a,i,it,ii in identifying_initial) # fr:29906
len(no_initials) # fr: 6016, de: 8486
len(one_initial_orphelins) # fr: 397, de:462
sum(two_most_likely_initial_not_in_title_initials) # fr: 36, de 76
sum(ii is not None for a,i,it,ii in identifying_initial)+len(no_initials)+len(one_initial_orphelins)+sum(two_most_likely_initial_not_in_title_initials) # fr: 29906+6016+397+36 = 36355
# %%



bugged_ids = {
    "de": [
        "012199", "012463", "029202", "012509", "058090", "041455", "020785", "020786",
        "020787", "020589", "020590", "011635", "020772", "012584", "012583", "020793",
        "012614", "029215", "029199", "029200", "029209", "012635", "029219", "029217",
        "029210", "046529", "019681"
    ],
    "fr": [
        "058089", "058090", "044498", "031336", "048634", "048313", "044235", "027390",
        "049777"
    ]
}

bugged_articles = [a for a in articles if a.id in bugged_ids[lng]]

# %%

[(a.id, a.title) for a in bugged_articles]

# %%


for a in bugged_articles:
    print(f"{a.id} '{a.title}' initial: {a.initial}")
    print(a.text+"\n\n\n")

# %%

for a in bugged_articles:
    initial = a.parse_identifying_initial()
    print(f"{a.id} initial={initial}\n\n")
# %%

a = bugged_articles[0]
a.parse_identifying_initial()

# %%

if lng=="de":
    napo = [a for a in bugged_articles if a.id=="041455"][0]
# %%
