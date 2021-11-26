from os import path

JSON_DUMPS_DIR = "../scrape-dhs/data/"

DHS_DUMP_JSONL_FILE = path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_all_articles_content.jsonl")

CATEGORIES = [
    ("themes", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_themes_articles.jsonl")),
    ("people", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_people_articles.jsonl")),
    ("families", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_families_articles.jsonl")),
    ("spatial", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_spatial_articles.jsonl"))
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


spacy_models_by_lng = {
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    "de": "de_core_news_sm",
}