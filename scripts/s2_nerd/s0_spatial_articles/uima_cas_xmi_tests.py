


# %%
from os import path
from random import sample, seed

import json
from langcodes import tag_match_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cassis as cassiss

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, DhsTag, tag_tree, DHS_ARTICLE_CATEGORIES
from inception_fishing import * 
from data_file_paths import *
from plot_styles import *

# %%

# Good intro to tokenizers: https://huggingface.co/docs/transformers/main/tokenizer_summary

# %%

inception_2022_annotation_folder = path.join(DATA_FOLDER,"inception_2022","annotation")
document_folder_path = path.join(inception_2022_annotation_folder,"000012_Rifferswil.txt")
typesystem_file_path = path.join(document_folder_path, "TypeSystem.xml")
annotated_file_path = path.join(document_folder_path, "dddpt.xmi")

# %%
with open(typesystem_file_path, "rb") as f:
        typesystem = cassiss.load_typesystem(f)

# %%

with open(annotated_file_path, "rb") as f:
    rifferswil = cassiss.load_cas_from_xmi(f,typesystem)

# %%

annotations = rifferswil.select_all()

# get the text!
annot_text = rifferswil.sofa_string


# %%
a0 = annotations[0]
# xmiId<->xmi:id allows to easily find which tag in the xmi the annotation corresponds to it is 
a0.xmiID
# get the tag tagtype!
a0.type.name
# begin/end
a0.begin
a0.end
# also accessible using the value() method
a0.value("begin")
# use get() to obtain xml tag attributes
a0.get("documentId")
a0.get("documentUri")
a0.get("documentTitle")
# get annotation text!
a0.get_covered_text()

# %%

a1 = annotations[1]
a1.xmiID
a1.type.name

# %%

annotations_types = {
    a.type.name
    for a in annotations
}
annotations_count = {
    t: sum([a.type.name==t for a in annotations])
    for t in annotations_types
}
annotations_count

# %%

token_type = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"

tokens_dtf = pd.DataFrame([
    (a.get_covered_text(), a.begin,a.end)
    for a in annotations if a.type.name==token_type
    ],
    columns=["text","begin","end"]
)
# %%


inception_2022_annotation_ser_folder = path.join(DATA_FOLDER,"inception_2022","annotation_ser")
ser_document_folder_path = path.join(inception_2022_annotation_ser_folder,"000033_Thalheim an der Thur.txt")
annotated_ser_file_path = path.join(ser_document_folder_path, "dddpt.ser")

with open(annotated_ser_file_path, "rb") as f:
    thalheim_ser = cassiss.load_cas_from_xmi(f,typesystem)

# %%



if False:
    def rebuilt_to_xmi(page: dict,  # todo : should this accept CommentaryPage objects ?
                    output_dir: str,
                    typesystem_path: str = PATHS['typesystem'],
                    iiif_mappings=None,
                    pct_coordinates=False):
        """
        Converts a rebuilt page into Apache UIMA/XMI format.
        The resulting file will be named after the page ID, adding
        the `.xmi` extension.
        :param page: the page to be converted
        :param output_dir: the path to the output directory
        :param typesystem_path: TypeSystem file containing defitions of annotation layers.
        """

        with open(typesystem_path, "rb") as f:
            typesystem = load_typesystem(f)  # object for the type system

        cas = Cas(typesystem=typesystem)
        cas.sofa_string = page["fulltext"]  # str # `ft` field in the rebuild CI
        cas.sofa_mime = 'text/plain'

        sentence = typesystem.get_type('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence')
        word = typesystem.get_type('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token')

        img_link_type = 'webanno.custom.AjMCImages'
        image_link = typesystem.get_type(img_link_type)

        # create sentence-level annotations
        for offsets in page["offsets"]["lines"]:
            cas.add_annotation(sentence(begin=offsets[0], end=offsets[1]))

        for offsets in page["offsets"]["words"]:
            cas.add_annotation(word(begin=offsets[0], end=offsets[1]))

        iiif_links = compute_image_links(page, iiif_links=iiif_mappings, pct=pct_coordinates)

        # inject the IIIF links into
        for iiif_link, start, end in iiif_links:
            cas.add_annotation(image_link(begin=start, end=end, link=iiif_link))

        outfile_path = os.path.join(output_dir, f'{page["id"]}.xmi')
        cas.to_xmi(outfile_path, pretty_print=True)