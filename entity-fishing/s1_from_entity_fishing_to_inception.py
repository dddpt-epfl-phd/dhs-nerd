from os import path
from lxml import etree

from inception_fishing import *

from utils import ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER, ENTITY_FISHING_ANNOTATION_OUTPUT_FILE, INCEPTION_IMPORT_FOLDER

# %%

language = "fr"




# %% importing from EF
with open(ENTITY_FISHING_ANNOTATION_OUTPUT_FILE) as entity_fishing_xml_file:
    entity_fishing_xml_root = etree.parse(entity_fishing_xml_file).getroot()
    corpus = Corpus.entity_fishing_from_tag_and_corpus(entity_fishing_xml_root, ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER)



# %% output to inception format

inception_tagset_tag_str = '<type2:TagsetDescription xmi:id="1780" sofa="1" begin="0" end="0" layer="webanno.custom.Entityfishinglayer" name="Grobid-NER" input="false"/>'

for d in corpus.documents:
    print(f"doing Document  {d.name}")
    d.inception_to_xml_file(INCEPTION_IMPORT_FOLDER, force_single_sentence=True, tagset_tag_str=inception_tagset_tag_str, tag_name="custom:Entityfishinglayer", identifier_attribute_name="wikidataidentifier")
# %%
