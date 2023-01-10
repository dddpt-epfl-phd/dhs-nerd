# %%
import unicodedata
from cassis import load_typesystem, Cas
from os import path

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from inception_fishing import Annotation
from inception_fishing import spacy as spacyIO

# %%

from ipynb.fs.full. s3_rule_based_annotation import *
#from s3_rule_based_annotation import *

# %%

"""

Steps:
- transform document to UIMA CAS
"""

# %%

spacyIO.document_add_tokens_as_annotations(
    sampled_articles_dtf.iloc[0,:].document,
    sampled_articles_dtf.iloc[0,:].tokens
)
sampled_articles_dtf.iloc[32,:].document.annotations
# %%

for i, row in sampled_articles_dtf.iterrows():
    spacyIO.document_add_tokens_as_annotations(
        row.document,
        row.tokens
    )

# %%

typesystem_path = "../../../data/inception_2022/LOC/TypeSystem.xml" 
# scripts/s2_nerd/s0_spatial_articles/s4_output_to_inception.py

with open(typesystem_path, "rb") as f:
        typesystem = load_typesystem(f)

# %%

def document_to_uima_cas(document, typesystem):
    """outputs a document to a cassis Cas object, ready to be written to a UIMA CAS xmi file.
    
    Annotations to be uima-cased:
    - tokens
        -> simply translate to generic token
    - polities
        -> need to translate polity-id to some kind of URI/identifier attribute
    """
    
    cas = Cas(typesystem=typesystem)
    cas.sofa_string = document.text
    cas.sofa_mime = 'text/plain'

    # Adding tokens
    token_type = typesystem.get_type("de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token")
    for a in document.annotations:
        if a.extra_fields.get("type")=="spacy_token":
            cas.add(token_type(begin=a.start, end=a.end))

    # Adding detected LOCs
    token_type = typesystem.get_type("de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity")
    for a in document.annotations:
        if a.extra_fields.get("type")=="polity_id_LOC":
            cas.add(token_type(begin=a.start, end=a.end, value="LOC", identifier=a.extra_fields.get("polity_id")))


    return cas

# %%

for i, row in sampled_articles_dtf.iterrows():
    
    casdoc = document_to_uima_cas(row.document, typesystem)
    
    cas_path = path.join(s2_polities_uima_cas_folder,row.hds_article_id+"_"+row.article_title+".xmi")
    casdoc.to_xmi(cas_path, pretty_print=True)

# %%

# %%
