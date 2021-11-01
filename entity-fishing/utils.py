from os import path

JSON_DUMPS_DIR = "../scrape-dhs/data/"

DHS_DUMP_JSONL_FILE = path.join(JSON_DUMPS_DIR, f"dhs_<LANGUAGE>_all_articles_content.jsonl")

CATEGORIES = [
    ("themes", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_themes_articles.jsonl")),
    ("people", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_people_articles.jsonl")),
    ("families", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_families_articles.jsonl")),
    ("spatial", path.join(JSON_DUMPS_DIR, f"dhs_fr_category_spatial_articles.jsonl"))
]

def get_dhs_dump_jsonl_file(language):
    return DHS_DUMP_JSONL_FILE.replace("<LANGUAGE>", language)