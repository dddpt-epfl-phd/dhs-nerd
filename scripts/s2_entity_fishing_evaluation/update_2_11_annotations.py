# %%
from webbrowser import open

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import Document
from s3_prepare_evaluation import load_pred_true_files_for_evaluation, evaluation_2_11
from s0_sample_dhs_articles_for_evaluation import sampled_articles_by_language

sampled_languages = ["fr", "de"]

"""
A first annotation has been finished on 2.11.2021.
In the meantime, the text extraction from DHS articles has changed (mainly adding the title to the main text)
This script is here to re-shift annotated document from 2.11 to correspond to new articles text

"""


# %% get annotated articles

def articles_sort_key(article):
    return article.title

annotated_articles_by_language = dict()
for lng in sampled_languages:
    sampled_articles_by_language[lng].sort(key=articles_sort_key)

    annotated_articles_by_language[lng] = [a for a in sampled_articles_by_language[lng][0:10] if a.id!="012281"]

# %%
if False:
    for article in annotated_articles_by_language["fr"]:
        open(article.url)
# -> all articles except Aventicum & Danube are single paragraph
# -> only Aventicum has intermediary paragraphs.

# %%

lng = "fr"

# %%

predicted_corpora_by_lng, annotated_corpora_by_lng = load_pred_true_files_for_evaluation(
        **evaluation_2_11
)

# %%

[a.title for a in annotated_articles_by_language[lng]]
[d.name for d in annotated_corpora_by_lng[lng].documents]

# %%


def get_dhsarticle_document_texts(document, article):
    new_document_text = article.title +". "+ document.text.replace("\n\n", " ") +" " 
    document_text = Document.from_dhs_article(
        article,
        p_text_blocks_separator=" ",
        non_p_text_blocks_separator=". "
    ).text

    lendiff = len(new_document_text) - len(document_text)
    if lendiff>0:
        document_text = document_text + lendiff*"X"
    elif lendiff<0:
        new_document_text = new_document_text + (-lendiff)*"X"
    return (new_document_text, document_text)

def show_dhsarticle_document_text_diff(document, article):
    """"""
    new_document_text, article_text = get_dhsarticle_document_texts(document, article)

    print(f"{article.title}: all Xs are characters that do not match between corpora and DhsArticle text:\n---")
    print("".join([c if new_document_text[i]==c else "X" for i,c in enumerate(article_text)]))

def count_dhsarticle_document_text_diff(document, article):
    new_document_text, article_text = get_dhsarticle_document_texts(document, article)
    return sum([new_document_text[i]!=c  for i,c in enumerate(article_text)])


# %%

new_document_text, document_text = get_dhsarticle_document_texts(annotated_corpora_by_lng[lng].documents[0], annotated_articles_by_language[lng][0])
show_dhsarticle_document_text_diff(annotated_corpora_by_lng[lng].documents[0], annotated_articles_by_language[lng][0])
count_dhsarticle_document_text_diff(annotated_corpora_by_lng[lng].documents[0], annotated_articles_by_language[lng][0])
# %%

for i, a in enumerate(annotated_articles_by_language[lng]):
    doc = annotated_corpora_by_lng[lng].documents[i]
    nbdiff = count_dhsarticle_document_text_diff(doc, a)
    print(f"{i}) article {a.title} <-> doc {doc.name}\n\tnumber of character discrepancies: {nbdiff}")

# %%
# %%
