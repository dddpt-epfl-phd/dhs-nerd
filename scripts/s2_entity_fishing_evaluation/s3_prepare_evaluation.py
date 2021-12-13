# %%
from os import path

from lxml import etree
import spacy

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import *
from utils import spacy_models_by_lng
from data_file_paths import  S2_INCEPTION_ANNOTATIONS_2_11_FOLDER, S2_INCEPTION_USER_NAME, S2_ENTITY_FISHING_2_11_OWN_EVALUATION_TRUE_FILE, S2_CLEF_HIPE_PRED_FILE, S2_CLEF_HIPE_TRUE_FILE, S2_ENTITY_FISHING_2_11_PREDICTION_OUTPUT_FILE, S2_ENTITY_FISHING_2_11_RAWTEXT_FOLDER, localize



"""
TODO:
- non grobid tag classes
- unlinked annotations
- embedded annotations
"""

sampled_languages = ["fr", "de"]

# %% spacy nlp by language
spacy_nlp_by_lng = dict()


# %% Load annotated corpus
def load_true_corpora_by_lng(
    in_inception_annotation_folder = S2_INCEPTION_ANNOTATIONS_2_11_FOLDER,
    in_inception_user_name = S2_INCEPTION_USER_NAME,
    sampled_languages = ["fr", "de"],
    in_inception_corpora_treatment = None,
    **kwargs
):


    # Load annotated corpus

    annotated_corpora_by_lng = inception.corpus_from_directory(
        "temp_corpus",
        in_inception_annotation_folder,
        in_inception_user_name
    )

    annotated_corpora_by_lng = {
        lng: Corpus(
            f"dhs-{lng}-true",
            [d for d in annotated_corpora_by_lng.documents if "."+lng+"." in d.name]
        ) for lng in sampled_languages
    }

    if in_inception_corpora_treatment is not None:
        print(f"load_true_corpora_by_lng() doing in_inception_corpora_treatment: {in_inception_corpora_treatment}")
        annotated_corpora_by_lng = in_inception_corpora_treatment(annotated_corpora_by_lng)

    return annotated_corpora_by_lng


# %% load_pred_true_files_for_evaluation

def load_pred_true_files_for_evaluation(
    in_inception_annotation_folder,
    in_inception_user_name,
    in_inception_corpora_treatment,
    in_entity_fishing_prediction_file,
    in_entity_fishing_rawtext_folder,
    in_entity_fishing_corpora_treatment,
    sampled_languages = ["fr", "de"],
    **kwargs
):
    # loading inception annotated corpora
    print("LOADING ANNOTATED CORPORA...")
    annotated_corpora_by_lng = load_true_corpora_by_lng(in_inception_annotation_folder, in_inception_user_name)

    # loading entity-fishing predicted corpora
    print("LOADING ef PREDICTED CORPORA...")
    predicted_corpora_by_lng = dict()
    for language in sampled_languages:
        with open(localize(in_entity_fishing_prediction_file, language)) as entity_fishing_xml_file:
            entity_fishing_xml_root = etree.parse(entity_fishing_xml_file).getroot()
            corpus = entity_fishing.corpus_from_tag_and_corpus(entity_fishing_xml_root, localize(in_entity_fishing_rawtext_folder, language))

        predicted_corpora_by_lng[language] = corpus
    if in_entity_fishing_corpora_treatment is not None:
        print(f"load_pred_true_files_for_evaluation() doing in_entity_fishing_corpora_treatment: {in_entity_fishing_corpora_treatment}")
        predicted_corpora_by_lng = in_entity_fishing_corpora_treatment(predicted_corpora_by_lng)

    return (predicted_corpora_by_lng, annotated_corpora_by_lng)

# %% write_annotated_corpora_for_evaluation
def write_annotated_corpora_for_evaluation(
    annotated_corpora_by_lng,
    clef_hipe_true_file = S2_CLEF_HIPE_TRUE_FILE,
    entity_fishing_true_xml = S2_ENTITY_FISHING_2_11_OWN_EVALUATION_TRUE_FILE,
    **kwargs
    ):
    for language, corpus in annotated_corpora_by_lng.items():
        corpus.set_annotations_wikipedia_page_titles_and_ids(language)

        if language not in spacy_nlp_by_lng:
            spacy_nlp_by_lng[language] = spacy.load(spacy_models_by_lng[language])

        # write conllu for clef-hipe-scorer
        corpus.clef_hipe_scorer_to_conllu_tsv(
            localize(clef_hipe_true_file, language),
            spacy_nlp_by_lng[language], language=language
        )

        # write entity-fishing xml for EF evaluation
        entity_fishing.corpus_to_xml_file(corpus, entity_fishing_true_xml)

# %% write_annotated_corpora_for_evaluation
def write_predicted_corpora_for_evaluation(predicted_corpora_by_lng, out_clef_hipe_pred_file, **kwargs):

    # writing predicted corpora
    print("WRITING EF PREDICTED CORPORA...")
    for language, corpus in predicted_corpora_by_lng.items():
        if language not in spacy_nlp_by_lng:
            spacy_nlp_by_lng[language] = spacy.load(spacy_models_by_lng[language])
        corpus.clef_hipe_scorer_to_conllu_tsv(
            localize(out_clef_hipe_pred_file, language),
            spacy_nlp_by_lng[language], language=language
        )

# %% load_and_write_pred_true_files_for_evaluation

def load_and_write_pred_true_files_for_evaluation(
    in_inception_annotation_folder,
    in_inception_user_name,
    in_inception_corpora_treatment,
    in_entity_fishing_prediction_file,
    in_entity_fishing_rawtext_folder,
    in_entity_fishing_corpora_treatment,
    out_entity_fishing_true_xml,
    out_clef_hipe_true_file,
    out_clef_hipe_pred_file,
    sampled_languages = ["fr", "de"]
):

    predicted_corpora_by_lng, annotated_corpora_by_lng = load_pred_true_files_for_evaluation(
        in_inception_annotation_folder,
        in_inception_user_name,
        in_inception_corpora_treatment,
        in_entity_fishing_prediction_file,
        in_entity_fishing_rawtext_folder,
        in_entity_fishing_corpora_treatment,
        sampled_languages
    )

    # writing annotated corpora
    print("WRITING ANNOTATED CORPORA...")
    write_annotated_corpora_for_evaluation(
        annotated_corpora_by_lng,
        out_clef_hipe_true_file, 
        out_entity_fishing_true_xml
    )
    
    # writing predicted corpora
    write_predicted_corpora_for_evaluation(predicted_corpora_by_lng, out_clef_hipe_pred_file)

# %% evaluation_2_11_annotation_treatment

def evaluation_2_11_true_treatment(annotated_corpora_by_lng):

    for language in sampled_languages:

        corpus = annotated_corpora_by_lng[language]

        # list of grobid_tags present:

        set(a.grobid_tag for d in corpus.documents for a in d.annotations)

        # most titles hand annotation should be thrown out as they do not interest us.
        set(a for d in corpus.documents for a in d.annotations if a.grobid_tag=="TITLE")


        # Remove unwanted annotations
        for d in corpus.documents:
            # ensure single spaces
            d.replace_regex("(\n| ){2,}", " ")
            d.replace_regex("'", '"')
            # Remove non-grobid tag classes
            d.annotations = [a for a in d.annotations if a.grobid_tag not in DHS_NERD_EXTRA_TAGS]
            # Remove SUBSTANCE,  ARTIFACT and TITLE
            # TITLE might need refining (keep duke of savoy or bishop of geneva)  
            d.annotations = [a for a in d.annotations if a.grobid_tag not in ["SUBSTANCE", "ARTIFACT", "TITLE"]]
            # Remove unlinked annotations
            d.annotations = [a for a in d.annotations if a.wikidata_entity_url is not None]
            # remove nested annotations
            d.remove_nested_annotations()
            d.update_mentions()

    return annotated_corpora_by_lng


    # %%

evaluation_2_11 = {
    #"corpus_name": "inception-annotation-2-11",
    "in_inception_annotation_folder": S2_INCEPTION_ANNOTATIONS_2_11_FOLDER,
    "in_inception_user_name": S2_INCEPTION_USER_NAME,
    "in_inception_corpora_treatment": evaluation_2_11_true_treatment,
    "in_entity_fishing_prediction_file": S2_ENTITY_FISHING_2_11_PREDICTION_OUTPUT_FILE,
    "in_entity_fishing_rawtext_folder": S2_ENTITY_FISHING_2_11_RAWTEXT_FOLDER,
    "in_entity_fishing_corpora_treatment": lambda x: x,
    "out_entity_fishing_true_xml": S2_ENTITY_FISHING_2_11_OWN_EVALUATION_TRUE_FILE,
    "out_clef_hipe_true_file": S2_CLEF_HIPE_TRUE_FILE,
    "out_clef_hipe_pred_file": S2_CLEF_HIPE_PRED_FILE,
}

#annotated_corpora_by_lng = load_true_corpora_by_lng("inception-annotation-2-11")

# %%


if __name__=="__main__":
    load_and_write_pred_true_files_for_evaluation(**evaluation_2_11)
