# all file paths relative to two folders up from the git repo root (../../path/from/git/repo/root)
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



# s2_entity_fishing/spacy_cassis_exploration
'inception-annotation-2-11/Daniel de Chambrier.fr.txt/dddpt.xmi'

# s2_entity_fishing/s0...py
ARTICLES_SAMPLE_DIRECTORY = f"entity-fishing/data/corpus/corpus-long/dhs-training-<LANGUAGE>/RawText/"

# s2_entity_fishing/utils.py
JSON_DUMPS_DIR = "../scrape-dhs/data/"

DHS_DUMP_JSONL_FILE = path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_all_articles_content.jsonl")

CATEGORIES = [
    ("themes", path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_category_themes_articles.jsonl")),
    ("people", path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_category_people_articles.jsonl")),
    ("families", path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_category_families_articles.jsonl")),
    ("spatial", path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_category_spatial_articles.jsonl"))
]

WIKIDATA_DHS_CSV_FILE = "../wikidata_dhs_linking/wikidata_dhs_wikipedia_articles_gndid.csv"


ENTITY_FISHING_CORPUS_FOLDER = f"entity-fishing/data/corpus/corpus-long/dhs-training-<LANGUAGE>/"
ENTITY_FISHING_ANNOTATION_OUTPUT_FILE = path.join(ENTITY_FISHING_CORPUS_FOLDER,f"dhs-training-<LANGUAGE>.xml")
ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER = path.join(ENTITY_FISHING_CORPUS_FOLDER, "RawText/")

SCORING_DATA_FOLDER = "scoring_data/"

INCEPTION_IMPORT_FOLDER = "inception-import-xml/"
INCEPTION_EXPORT_FOLDER = "inception-annotation-2-11"
INCEPTION_USER_NAME = "dddpt"

def localize(path, language):
    return path.replace("<LANGUAGE>", language)
