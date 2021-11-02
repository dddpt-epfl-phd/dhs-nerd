from os import path
from lxml import etree

from inception_fishing import *


# %%

language = "fr"

entity_fishing_corpus_folder = f"entity-fishing/data/corpus/corpus-long/dhs-training-{language}/"
entity_fishing_annotation_output_file = path.join(entity_fishing_corpus_folder,f"dhs-training-{language}.xml")
entity_fishing_corpus_rawtext_folder = path.join(entity_fishing_corpus_folder, "RawText/")



# %% importing from EF
with open(entity_fishing_annotation_output_file) as entity_fishing_xml_file:
    entity_fishing_xml_root = etree.parse(entity_fishing_xml_file).getroot()
    corpus = Corpus.entity_fishing_from_tag_and_corpus(entity_fishing_xml_root, entity_fishing_corpus_rawtext_folder)



# %% output to inception format

inception_tagset_tag_str = '<type2:TagsetDescription xmi:id="1780" sofa="1" begin="0" end="0" layer="webanno.custom.Entityfishinglayer" name="Grobid-NER" input="false"/>'

inception_import_folder = "inception-import-xml/"
for d in corpus.documents:
    print(f"doing Document  {d.name}")
    d.inception_to_xml_file(inception_import_folder, force_single_sentence=True, tagset_tag_str=inception_tagset_tag_str, tag_name="custom:Entityfishinglayer", identifier_attribute_name="wikidataidentifier")
# %%
