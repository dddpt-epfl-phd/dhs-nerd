# %%
from functools import reduce
from random import sample, seed

from lxml import html
from lxml.etree import iselement
from webbrowser import open as op

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from dhs_scraper import DhsArticle
from data_file_paths import localize, S0_JSONL_ALL_ARTICLES_FILE, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES

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
links = [e.cssselect("a") for e in elements]
links_flat = [a for ases in links for a in ases]


# %%

for t in elements[3].iter():
    print(f"LEVEL 0: <{t.tag}> {t.text_content()}")
    for t1 in t:
        print(f"- <{t1.tag}> {t1.text_content()}")

# %%

for node in elements[3].xpath("child::node()"):
    print(f"NODE: {node} iselement: {iselement(node)}")

# %%
for t in elements[3].iterlinks():
    print(t)
# %%
for t in elements[3].iterdescendants("*"):
    print(f"TEXT:\n{t}")
# %%
for t in elements[3].itertext():
    print(f"TEXT:\n{t}")

# %%

def lxml_depth_first_iterator(element, iteration_criterion):
    """iterate depth-first over an lxml element, yielding elements according to iteration_criterion()

    Considers both text and Element nodes.

    yields:
    - all descendants d of element for which iteration_criterion(d) returns True
    """
    for node in element.xpath("child::node()"):
        print(f"lxml_dpi() node: {node}, iteration_criterion(node): {iteration_criterion(node)}, iselement(node): {iselement(node)}")
        if iteration_criterion(node):
            yield node
        elif iselement(node):
            for n in lxml_depth_first_iterator(node, iteration_criterion):
                yield n

def is_text_or_link(node):
    if (not iselement(node)) or (node.tag=="a"):
        return True
    return False

text_and_links = [tl for tl in lxml_depth_first_iterator(elements[3], is_text_or_link)]
text_and_links

# %% Check results:

vaud.parse_text_links()
# -> good!

# %%


othon = DhsArticle(url="https://hls-dhs-dss.ch/fr/articles/017791/2008-01-21/")
othon.parse_text_links()
# -> good!

# %%
