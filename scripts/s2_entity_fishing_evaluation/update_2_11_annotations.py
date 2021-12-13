# %%
from webbrowser import open

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import Document
from data_file_paths import S2_INCEPTION_REIMPORT_2_11_FOLDER
from s3_prepare_evaluation import load_true_corpora_by_lng, evaluation_2_11
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
def documents_sort_key(doc):
    return doc.name

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
evaluation_2_11["in_inception_corpora_treatment"] = None
annotated_corpora_by_lng = load_true_corpora_by_lng(
        **evaluation_2_11
)
for lng in sampled_languages:
    annotated_corpora_by_lng[lng].documents.sort(key=documents_sort_key)
    

# %%

[a.title for a in annotated_articles_by_language[lng]]
[d.name for d in annotated_corpora_by_lng[lng].documents]

# %%

def update_2_11_annotated_document(document_2_11:Document, article):
    newdoc = document_2_11.__deepcopy__()
    newdoc.replace_span(0,0, article.title +". ")
    newdoc.replace_regex("  ", " ")
    newdoc.replace_span(len(newdoc.text),len(newdoc.text), " ")
    return newdoc


def get_dhsarticle_document_texts(document, article):
    #new_document_text = article.title +". "+ document.text.replace("\n\n", " ") +" " 
    new_document_text = update_2_11_annotated_document(document, article).text
    document_text = Document.from_dhs_article(
        article,
        p_text_blocks_separator=" ",
        non_p_text_blocks_separator=". "
    ).text

    lendiff = len(new_document_text) - len(document_text)
    if lendiff>0:
        print("LENDIFF ++++")
        document_text = document_text + lendiff*"X"
    elif lendiff<0:
        print("LENDIFF ----")
        new_document_text = new_document_text + (-lendiff)*"X"
    return (new_document_text, document_text)


def get_index_by_substring(documents, substr):
    for i, d in enumerate(documents):
        if substr in d.name:
            return i
def get_document_article_by_substring(documents, articles, substr):
    index = get_index_by_substring(documents, substr)
    return documents[index], articles[index]

def show_dhsarticle_document_text_diff(document, article):
    """"""
    new_document_text, article_text = get_dhsarticle_document_texts(document, article)

    print(f"{article.title}: all Xs are characters that do not match between corpora and DhsArticle text:\n---")
    print("".join([c if new_document_text[i]==c else "X" for i,c in enumerate(article_text)]))

def count_dhsarticle_document_text_diff(document, article):
    new_document_text, article_text = get_dhsarticle_document_texts(document, article)
    return sum([new_document_text[i]!=c  for i,c in enumerate(article_text)])


# %%

lng = "de"
substr = "Luginbühl"
da = get_document_article_by_substring(annotated_corpora_by_lng[lng].documents,  annotated_articles_by_language[lng], substr)
d=da[0]
a = da[1]
new_document_text, document_text = get_dhsarticle_document_texts(*da)
show_dhsarticle_document_text_diff(*da)
count_dhsarticle_document_text_diff(*da)
# %%

for lng in annotated_corpora_by_lng.keys():
    for i, a in enumerate(annotated_articles_by_language[lng]):
        doc = annotated_corpora_by_lng[lng].documents[i]
        nbdiff = count_dhsarticle_document_text_diff(doc, a)
        print(f"{i}) article {a.title} <-> doc {doc.name}\n\tnumber of character discrepancies: {nbdiff}")

# %%
# %%

if __name__=="__main__":
    for lng, corpus in annotated_corpora_by_lng.items():
        inception_tagset_tag_str = '<type2:TagsetDescription xmi:id="1780" sofa="1" begin="0" end="0" layer="webanno.custom.Entityfishinglayer" name="Grobid-NER" input="false"/>'

        if __name__=="__main__":
            for i,d in enumerate(corpus.documents):
                a = annotated_articles_by_language[lng][i]
                new_d = update_2_11_annotated_document(d, a)
                print(f"doing Document  {d.name}")
                new_d.inception_to_xml_file(S2_INCEPTION_REIMPORT_2_11_FOLDER, force_single_sentence=True, tagset_tag_str=inception_tagset_tag_str, tag_name="custom:Entityfishinglayer", identifier_attribute_name="wikidataidentifier")
