# %%
from os import path

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
        "dhs-training-fr",
        [d for d in annotated_corpora_lng.documents if "."+lng+"." in d.name]
    ) for lng in sampled_languages
}

annotated_corpora_lng

DHS_NERD_ANNOTATIONS_TAGS
DHS_NERD_EXTRA_TAGS

lng = "de"

corpus = annotated_corpora_lng[lng]

# %% list of grobid_tags present:

set(a.grobid_tag for d in corpus.documents for a in d.annotations)

# %%

# most titles hand annotation should be thrown out as they do not interest us.
set(a for d in corpus.documents for a in d.annotations if a.grobid_tag=="TITLE")


# %% Remove unwanted annotations

for d in corpus.documents:
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

# %% Writing back to file

corpus.set_annotations_wikipedia_page_titles_and_ids(lng)

corpus.entity_fishing_to_xml_file(path.join(INCEPTION_EXPORT_FOLDER,f"dhs-training-{lng}.xml"))

# %%
