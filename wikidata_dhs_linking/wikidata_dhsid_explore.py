# %%
import re

import matplotlib
import pandas as pd

# %%

wd = pd.read_csv("wikidata_dhs_wikipedia_articles_gndid_instanceof.csv")
wd.rename(columns={'itemLabel':'itemLabel_fr'}, inplace=True)
wd_de = pd.read_csv("wikidata_de_labels.csv")
wd_de.rename(columns={'itemLabel':'itemLabel_de'}, inplace=True)

wd = wd.merge(wd_de, on=["dhsid","item"])

# %%



missing_label_regex = re.compile(r"^Q\d+$")
wd["missing_itemLabel_fr"] = wd.itemLabel_fr.apply(lambda label: missing_label_regex.match(label) is not None)
wd["missing_itemLabel_de"] = wd.itemLabel_de.apply(lambda label: missing_label_regex.match(label) is not None)

# %%

print(f"number of articles with dhsid: {wd.shape}. Number of distinct dhsid in wd: {wd.dhsid.unique().shape}")

# %%

languages = ["fr", "de", "it", "en"]



nb_missing_articles_bag = dict()
nb_exclusive_articles = dict()
wd["nb_articles_across_languages"] = 0
for i1, lng1 in enumerate(languages):
    wd["nopage"+lng1] = wd["article"+lng1].isnull()
    nb_missing_articles_bag[lng1] = wd["nopage"+lng1].sum()
    wd["nb_articles_across_languages"] = wd["nb_articles_across_languages"] + (~wd["article"+lng1].isnull())
    for i2, lng2 in enumerate(languages[(i1+1):len(languages)]):
        wd["nopage"+lng1+lng2] = wd["article"+lng1].isnull() & wd["article"+lng2].isnull()
        nb_missing_articles_bag[lng1+lng2] = wd["nopage"+lng1+lng2].sum()
        for i3, lng3 in enumerate(languages[(i1+i2+2):len(languages)]):
            wd["nopage"+lng1+lng2+lng3] = wd["article"+lng1].isnull() & wd["article"+lng2].isnull() & wd["article"+lng3].isnull()
            nb_missing_articles_bag[lng1+lng2+lng3] = wd["nopage"+lng1+lng2+lng3].sum()
            for i4, lng4 in enumerate(languages[(i1+i2+i3+3):len(languages)]):
                wd["nopage"+lng1+lng2+lng3+lng4] = wd["article"+lng1].isnull() & wd["article"+lng2].isnull() & wd["article"+lng3].isnull() & wd["article"+lng4].isnull()
                nb_missing_articles_bag[lng1+lng2+lng3+lng4] = wd["nopage"+lng1+lng2+lng3+lng4].sum()
                wd["onlypage"+lng1] = (~wd["article"+lng1].isnull()) & wd["article"+lng2].isnull() & wd["article"+lng3].isnull()  & wd["article"+lng4].isnull() 
                wd["onlypage"+lng2] = (~wd["article"+lng2].isnull()) & wd["article"+lng1].isnull() & wd["article"+lng3].isnull()  & wd["article"+lng4].isnull() 
                wd["onlypage"+lng3] = (~wd["article"+lng3].isnull()) & wd["article"+lng2].isnull() & wd["article"+lng1].isnull()  & wd["article"+lng4].isnull() 
                wd["onlypage"+lng4] = (~wd["article"+lng4].isnull()) & wd["article"+lng2].isnull() & wd["article"+lng3].isnull()  & wd["article"+lng1].isnull() 
    nb_exclusive_articles[lng1] = wd["onlypage"+lng1].sum()

nb_missing_articles_list = [(k2,v2) for k2,v2 in nb_missing_articles_bag.items()]
nb_missing_articles_list.sort(key=lambda t: len(t[0]))
nb_missing_articles = {k:v for k, v in nb_missing_articles_list}

print(f'nb of missing articles in each languages combination:\n{nb_missing_articles}')
print(f'nb of articles exclusive to each language:\n{nb_exclusive_articles}')



# %%

entity_types_counts = wd["instanceofLabel"].value_counts()

entity_types_counts[entity_types_counts>20]

# %%