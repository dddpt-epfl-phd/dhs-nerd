from os import path

from lxml import etree
import spacy

from inception_fishing import *
from utils import *

# %%


sampled_languages = ["fr", "de"]


predicted_corpora_by_lng = dict()

for language in sampled_languages:



    # %% importing from EF
    with open(localize(ENTITY_FISHING_ANNOTATION_OUTPUT_FILE, language)) as entity_fishing_xml_file:
        entity_fishing_xml_root = etree.parse(entity_fishing_xml_file).getroot()
        corpus = Corpus.entity_fishing_from_tag_and_corpus(entity_fishing_xml_root, localize(ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER, language))

    predicted_corpora_by_lng[language] = corpus

    # %%

    for d in corpus.documents:
        d.replace_regex("(\n| ){2,}", " ")

    # %% output to inception format

    inception_tagset_tag_str = '<type2:TagsetDescription xmi:id="1780" sofa="1" begin="0" end="0" layer="webanno.custom.Entityfishinglayer" name="Grobid-NER" input="false"/>'

    if __name__=="__main__":
        for d in corpus.documents:
            print(f"doing Document  {d.name}")
            d.inception_to_xml_file(INCEPTION_IMPORT_FOLDER, force_single_sentence=True, tagset_tag_str=inception_tagset_tag_str, tag_name="custom:Entityfishinglayer", identifier_attribute_name="wikidataidentifier")
    # %%



    nlp = spacy.load(spacy_models_by_lng[language])

    # %%


    if __name__=="__main__":
        corpus.clef_hipe_scorer_to_conllu_tsv(
            path.join(SCORING_DATA_FOLDER,f"dhs-{language}-pred-clef-hipe-scorer-conllu.tsv"),
            nlp, language=language
        )
