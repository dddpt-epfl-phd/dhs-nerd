# %%
from os import path

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import *
from utils import spacy_models_by_lng
from file_paths import  S2_INCEPTION_ANNOTATIONS_2_11_FOLDER, S2_INCEPTION_USER_NAME, S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER

# %% load original DhsArticles

#from s0_sample_dhs_training_data_for_entity_fishing import sampled_articles_by_language

"""
TODO:
- non grobid tag classes
- unlinked annotations
- embedded annotations
"""

sampled_languages = ["fr", "de"]

# %% Load annotated corpus

annotated_corpora_by_lng = Corpus.inception_from_directory(
    "inception-annotation-2-11",
    S2_INCEPTION_ANNOTATIONS_2_11_FOLDER,
    S2_INCEPTION_USER_NAME
)

annotated_corpora_by_lng = {
    lng: Corpus(
        f"dhs-{lng}-true",
        [d for d in annotated_corpora_by_lng.documents if "."+lng+"." in d.name]
    ) for lng in sampled_languages
}

annotated_corpora_by_lng

# %%


for language in sampled_languages:

    corpus = annotated_corpora_by_lng[language]

    # %% list of grobid_tags present:

    set(a.grobid_tag for d in corpus.documents for a in d.annotations)

    # %%

    # most titles hand annotation should be thrown out as they do not interest us.
    set(a for d in corpus.documents for a in d.annotations if a.grobid_tag=="TITLE")


    # %% Remove unwanted annotations

    for d in corpus.documents:
        # ensure single spaces
        d.replace_regex("(\n| ){2,}", " ")
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


    corpus.set_annotations_wikipedia_page_titles_and_ids(language)

    # %%


    import spacy

    nlp = spacy.load(spacy_models_by_lng[language])

    # %%

    if __name__=="__main__":

        corpus.clef_hipe_scorer_to_conllu_tsv(
            path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,corpus.name+"-clef-hipe-scorer-conllu.tsv"),
            nlp, language=language
        )


        corpus.entity_fishing_to_xml_file(path.join(S2_INCEPTION_ANNOTATIONS_2_11_FOLDER,corpus.name+"-entity-fishing-scorer.xml"))
