# %%

import json

import requests as r

import spacy

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")
sys.path.append("../../src/CLEF-HIPE-2020-scorer")

from inception_fishing import entity_fishing, dhs_article, wikipedia, inception, Corpus, Document, clef_hipe_scorer
from dhs_scraper import DhsArticle
from clef_evaluation import evaluation_wrapper, Evaluator, main

from data_file_paths import S2_INCEPTION_ANNOTATIONS_16_12_FOLDER, S2_INCEPTION_USER_NAME, S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER, S2_CLEF_HIPE_PRED_FILE_16_12, S2_CLEF_HIPE_TRUE_FILE_16_12 , localize, S2_CLEF_HIPE_TAGGED_FILE, S2_CLEF_HIPE_TAGGED_FILE
from s2_entity_fishing_evaluation.s0_sample_dhs_articles_for_evaluation import sampled_articles_by_language
from utils import spacy_models_by_lng

# %% spacy nlp by language
spacy_nlp_by_lng = dict()

"""
TODO TODO TODO TODO TODO TODO TODO TODO :
TODO TODO TODO TODO TODO TODO TODO TODO :
TODO TODO TODO TODO TODO TODO TODO TODO :
TODO TODO TODO TODO TODO TODO TODO TODO :
TODO TODO TODO TODO TODO TODO TODO TODO :
TODO TODO TODO TODO TODO TODO TODO TODO :
1) load annotated documents 
2) add last annotations (replace initials, article title)
3) launch prediction by EF of documents 
4) get evaluation scores
"""

# %%



# %% Load annotated corpus
def load_true_corpora_by_lng_16_12(
    in_inception_annotation_folder = S2_INCEPTION_ANNOTATIONS_16_12_FOLDER,
    in_inception_user_name = S2_INCEPTION_USER_NAME,
    sampled_languages = ["fr", "de"],
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

    # change initials & add titles annotations
    for lng in sampled_languages:
        for a in sampled_articles_by_language[lng]:
            for d in annotated_corpora_by_lng[lng].documents:
                if a.title in d.name:
                    print (f"a.title in d.name!! {a.title} in {d.name}")
                    dhs_article.document_replace_initial_from_dhs_article(d, a)
                    dhs_article.document_annotate_title_from_dhs_article(d, a)


    return annotated_corpora_by_lng

# %%


def get_unannotated_corpus(corpus):
    return Corpus(
        corpus.name.replace("true","pred"),
        [Document(d.name, [], d.text) for d in corpus.documents]
    )



# %%


annotated_corpora_by_lng = load_true_corpora_by_lng_16_12()




# %%

dalois = [d for d in annotated_corpora_by_lng["fr"].documents if "Alois" in d.name][0]
aalois = [d for d in sampled_articles_by_language["fr"] if "Alois" in d.title][0]




# %%


def evaluate(annotated_corpus:Corpus, language:str, filetag:str):
    # getting resutls from entity-fishing
    pred_corpus = get_unannotated_corpus(annotated_corpus)
    for d in pred_corpus.documents:
        print(f"predicting for document {d.name}")
        entity_fishing.document_named_entity_linking(d, language, include_entities=False)

    if language not in spacy_nlp_by_lng:
            spacy_nlp_by_lng[language] = spacy.load(spacy_models_by_lng[language])

    # writing files
    pred_file = localize(S2_CLEF_HIPE_TAGGED_FILE.replace("<TAG>", filetag).replace("<PREDTRUE>", "pred"), language)
    true_file = localize(S2_CLEF_HIPE_TAGGED_FILE.replace("<TAG>", filetag).replace("<PREDTRUE>", "true"), language)
    clef_hipe_scorer.corpus_to_conllu_tsv(
        pred_corpus,
        localize(pred_file, language),
        spacy_nlp_by_lng[language], language=language
    )
    clef_hipe_scorer.corpus_to_conllu_tsv(
        annotated_corpus,
        localize(true_file, language),
        spacy_nlp_by_lng[language], language=language
    )

    # using CLEF-HIPE scorer
    print(f"evaluating withh:\ntrue_file:{true_file}\npred_file:{pred_file}")
    if False:
        evaluator = Evaluator(true_file, pred_file, None)
        evaluation_wrapper(
            evaluator = evaluator,
            cols = ['NEL-LIT', 'NEL-METO'],
            eval_type = "nel",
            n_best = 1,
            noise_levels = [None],
            time_periods = [None],
            tags = None,
        )
    args = {'--glue': None,
    '--help': False,
    '--log': None,
    '--n_best': '1',
    '--noise-level': None,
    '--outdir': S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,
    '--pred': pred_file,
    '--ref': true_file,
    '--skip-check': True,
    '--suffix': None,
    '--tagset': None,
    '--task': 'nel',
    '--time-period': None}

    return (
        main(args),
        pred_corpus,
        annotated_corpus
    )

# %%

lng = "de"
results, pred_corpus, true_corpus = evaluate(annotated_corpora_by_lng[lng], lng, "16-12-test")


tdalen = [len(d.annotations) for d in true_corpus.documents]
dalen = [len(d.annotations) for d in pred_corpus.documents]
(tdalen, dalen)

results
# %%

# %%
