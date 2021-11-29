# %%
from functools import reduce
from random import sample, seed
import re

from lxml import html
import pandas as pd
from webbrowser import open as op

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from dhs_scraper import DhsArticle
from file_paths import localize, S0_JSONL_ALL_ARTICLES_FILE, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES

seed(54367)

# %%

lng="fr"


# %%


vaud = DhsArticle(url="https://hls-dhs-dss.ch/fr/articles/007395/2017-05-30/")
vaud.download_page_content()
# %%

# %%

vaud._pagetree = html.fromstring(vaud.page_content)

all_text_elements = vaud._pagetree.cssselect(".hls-article-text-unit p, h1, h2, .hls-article-text-unit h3, .hls-article-text-unit h4")

# %%
to_remove_p = vaud._pagetree.cssselect(".media-content p")
to_remove_elements = vaud._pagetree.cssselect(".media-content")
for tre in to_remove_elements:
    tre.getparent().remove(tre)
# %%

elements = vaud._pagetree.cssselect(".hls-article-text-unit p, h1, h2, .hls-article-text-unit h3, .hls-article-text-unit h4")
text = reduce(lambda s,el: s+el.text_content()+"\n\n", elements, "")[0:-2]
        


# %%
