from inception_fishing import *
from utils import INCEPTION_EXPORT_FOLDER, INCEPTION_USER_NAME

from s0_sample_dhs_training_data_for_entity_fishing import sampled_articles_by_language

"""
TODO:
- non grobid tag classes
- unlinked annotations
- embedded annotations
"""


inception_annotations = Corpus.inception_from_directory(
    "inception-annotation-2-11",
    INCEPTION_EXPORT_FOLDER,
    INCEPTION_USER_NAME
)

inception_annotations