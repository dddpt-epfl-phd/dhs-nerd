from inception_fishing import *
from utils import INCEPTION_EXPORT_FOLDER, INCEPTION_USER_NAME

# %% load original DhsArticles

from s0_sample_dhs_training_data_for_entity_fishing import sampled_articles_by_language

"""
TODO:
- non grobid tag classes
- unlinked annotations
- embedded annotations
"""

sampled_languages = ["fr", "de"]

# %% Load annotated corpus

annotated_corpora_lng = Corpus.inception_from_directory(
    "inception-annotation-2-11",
    INCEPTION_EXPORT_FOLDER,
    INCEPTION_USER_NAME
)

annotated_corpora_lng = {
    lng: Corpus(
        "inception-annotation-2-11-fr",
        [d for d in annotated_corpora_lng.documents if "."+lng+"." in d.name]
    ) for lng in sampled_languages
}

annotated_corpora_lng

DHS_NERD_ANNOTATIONS_TAGS
DHS_NERD_EXTRA_TAGS

lng = "fr"

corpus = annotated_corpora_lng[lng]


# %% Remove unwanted annotations

for d in corpus.documents:
    # Remove non-grobid tag classes
    d.annotations = [a for a in d.annotations if a.grobid_tag not in DHS_NERD_EXTRA_TAGS]
    # Remove unlinked annotations
    d.annotations = [a for a in d.annotations if a.wikidata_entity_url is not None]
    # remove nested annotations
    d.remove_nested_annotations()

# %%
