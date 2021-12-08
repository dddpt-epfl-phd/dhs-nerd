# %%
from os import path

from cassis import *
 
import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from data_file_paths import S2_INCEPTION_ANNOTATIONS_2_11_FOLDER
# %%

with open(path.join(S2_INCEPTION_ANNOTATIONS_2_11_FOLDER, 'Daniel de Chambrier.fr.txt/TypeSystem.xml'), 'rb') as f:
    typesystem = load_typesystem(f)

# %%

with open(path.join(S2_INCEPTION_ANNOTATIONS_2_11_FOLDER, 'Daniel de Chambrier.fr.txt/dddpt.xmi'), 'rb') as f:
   cas = load_cas_from_xmi(f, typesystem=typesystem)
# %%

EFL = typesystem.get_type("webanno.custom.Entityfishinglayer")

# %%

if False:
    for sentence in cas.select('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence'):
        for ef_annotation in cas.select_covered('webanno.custom.Entityfishinglayer', sentence):
            print(ef_annotation.get_covered_text())

            # Annotation values can be accessed as properties
            print('Token: begin={0}, end={1}, id={2}, tag={3}'.format(ef_annotation.begin, ef_annotation.end, ef_annotation.wikidataidentifier, ef_annotation.entityfishingtag))

# %%

# text content:
cas.sofa_string

# %%
import spacy

"""
efficient:
en_core_web_sm
fr_core_news_sm
de_core_news_sm
accurater but slower
en_core_web_trf
fr_dep_news_trf
de_dep_news_trf
"""

nlp = spacy.load("fr_core_news_sm")

doc = nlp(cas.sofa_string)
# %%

if False:
    for token in doc:
        print(f"-----\npos: {token.pos_}, text:\n{token.text} ")
"""
useful props:
- token.i: index (=i-th token in doc)
- token.idx: character pos of token in doc text
- token.text
- len(token) = len(token.text)
- token.sent: sentence of token

extensions: spacy custom attributes:
Doc.set_extension("hello", default=True)
assert doc._.hello
doc._.hello = False
"""
# %%

from s2_entity_fishing_evaluation.s3_prepare_evaluation import corpus

doc = corpus.documents[0]

print(corpus.clef_hipe_scorer_to_conllu_tsv(nlp))

# %%
