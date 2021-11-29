# all file paths relative to two folders up from the git repo root (../../path/from/git/repo/root)
from logging import RootLogger
from os import path
from typing import Tuple

# scripts are always assumed to be two directories down from root
ROOT_FOLDER = "../.."

DATA_FOLDER = path.join(ROOT_FOLDER, "data")
REPORTS_FOLDER = path.join(ROOT_FOLDER, "reports")

FIGURES_FOLDER = path.join(REPORTS_FOLDER, "figures")


# s0_scrape_dhs
#####################



S0_DATA_FOLDER = path.join(DATA_FOLDER, "scrape_dhs")

# s0_scrape_dhs/s0_scrape.py
S0_JSONL_ALL_ARTICLES_FILE = path.join(S0_DATA_FOLDER, "dhs_<LANGUAGE>_all_articles_content.jsonl")

S0_THEMES_CATEGORY = "themes"
S0_PEOPLE_CATEGORY = "people"
S0_FAMILIES_CATEGORY = "families"
S0_SPATIAL_CATEGORY = "spatial"
S0_DHS_CATEGORIES = [S0_THEMES_CATEGORY, S0_PEOPLE_CATEGORY, S0_FAMILIES_CATEGORY, S0_SPATIAL_CATEGORY]

S0_JSONL_ARTICLES_BY_CATEGORIES_FILES = {
    category: path.join(S0_DATA_FOLDER, f"dhs_<LANGUAGE>_category_{category}_articles.jsonl")
    for category in S0_DHS_CATEGORIES
}

# s0_scrape_dhs/s1_dhs_stats.py
s0_png_articles_lengths_by_category_figure = path.join(FIGURES_FOLDER, "articles_lengths_by_category.png")
s0_png_percent_articles_in_wd_by_category = path.join(FIGURES_FOLDER, "percent_articles_in_wd_by_category.png")


# s1_wikidata_dhs_linking
#####################

S1_DATA_FOLDER = path.join(DATA_FOLDER, "wikidata_dhs_linking")

S1_WIKIDATA_DHS_WIKIPEDIA_LINKS = path.join(S1_DATA_FOLDER, "wikidata_dhs_wikipedia_articles_gndid_instanceof.csv")
S1_WIKIDATA_DE_LABELS = path.join(S1_DATA_FOLDER, "wikidata_de_labels.csv")

# s2_entity_fishing
#####################
S2_INCEPTION_DATA_FOLDER = path.join(DATA_FOLDER, "inception")
S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER = path.join(DATA_FOLDER, "entity-fishing-evaluation")

S2_ENTITY_FISHING_CORPUS_FOLDER = path.join(ROOT_FOLDER, f"entity-fishing/entity-fishing/data/corpus/corpus-long/dhs-training-<LANGUAGE>/")
S2_ENTITY_FISHING_ANNOTATION_OUTPUT_FILE = path.join(S2_ENTITY_FISHING_CORPUS_FOLDER,f"dhs-training-<LANGUAGE>.xml")
S2_ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER = path.join(S2_ENTITY_FISHING_CORPUS_FOLDER, "RawText/")


S2_INCEPTION_IMPORT_FOLDER = path.join(S2_INCEPTION_DATA_FOLDER, "inception-import-xml/")
S2_INCEPTION_ANNOTATIONS_2_11_FOLDER = path.join(S2_INCEPTION_DATA_FOLDER, 'inception-annotation-2-11')
S2_INCEPTION_USER_NAME = "dddpt"

def localize(path, language):
    return path.replace("<LANGUAGE>", language)
