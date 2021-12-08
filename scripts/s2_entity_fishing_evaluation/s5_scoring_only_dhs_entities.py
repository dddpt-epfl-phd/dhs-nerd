# %%

from os import path
from csv import DictReader

import spacy

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import Corpus, Document, Annotation
from s2_entity_fishing_evaluation.s2_from_entity_fishing_to_inception import predicted_corpora_by_lng
from s2_entity_fishing_evaluation.s3_from_inception_annotation_to_entity_fishing import annotated_corpora_by_lng
from utils import spacy_models_by_lng
from file_paths import S1_WIKIDATA_DHS_WIKIPEDIA_LINKS, S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER
# %%



with open(S1_WIKIDATA_DHS_WIKIPEDIA_LINKS) as file:
    wikidata_entities = [ r for r in DictReader(file)]
dhs_wikidata_entities = set(e["item"] for e in wikidata_entities)
dhs_wikipedia_entities_by_lng = {
    "fr": set(e["item"] for e in wikidata_entities if e["articlefr"]!=""),
    "de": set(e["item"] for e in wikidata_entities if e["articlede"]!="")
}


sampled_languages = ["fr", "de"]

dhs_only_corpora_by_lng = dict()
dhs_wk_only_corpora_by_lng = dict()

# %%


def create_filtered_true_pred_tsv(pred_corpus, true_corpus, nlp, wikidata_entities_ids_to_keep, corpus_name_suffix = ""):

    pred_corpus_filtered = pred_corpus.__deepcopy__()
    pred_corpus_filtered.name = f"dhs-{language}-{corpus_name_suffix}-pred"
    for d in pred_corpus_filtered.documents:
        d.filter_annotations(lambda a: a.wikidata_entity_url in wikidata_entities_ids_to_keep)

    pred_corpus_filtered.clef_hipe_scorer_to_conllu_tsv(
        path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,pred_corpus_filtered.name+f"-clef-hipe-scorer-conllu.tsv"),
        nlp, language=language
    )

    true_corpus_filtered = true_corpus.__deepcopy__()
    true_corpus_filtered.name = f"dhs-{language}-{corpus_name_suffix}-true"
    for d in true_corpus_filtered.documents:
        d.filter_annotations(lambda a: a.wikidata_entity_url in wikidata_entities_ids_to_keep)
    true_corpus_filtered.clef_hipe_scorer_to_conllu_tsv(
        path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,true_corpus_filtered.name+"-clef-hipe-scorer-conllu.tsv"),
        nlp, language=language
    )
    return (pred_corpus_filtered, true_corpus_filtered)

# %%

for language in sampled_languages:
    nlp = spacy.load(spacy_models_by_lng[language])

    pred_corpus:Corpus = predicted_corpora_by_lng[language]
    true_corpus:Corpus = annotated_corpora_by_lng[language]

    dhs_only_corpora_by_lng[language] = create_filtered_true_pred_tsv(pred_corpus, true_corpus, nlp, dhs_wikidata_entities, "only-dhs-wd")
    dhs_wk_only_corpora_by_lng[language] = create_filtered_true_pred_tsv(pred_corpus, true_corpus, nlp, dhs_wikipedia_entities_by_lng[language], f"only-dhs-wk{language}")

    # %%
