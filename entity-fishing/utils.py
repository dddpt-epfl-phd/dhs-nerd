
DHS_DUMP_JSONL_FILE = f"../scrape-dhs/data/dhs_<LANGUAGE>_all_articles_content.jsonl"

def get_dhs_dump_jsonl_file(language):
    return DHS_DUMP_JSONL_FILE.replace("<LANGUAGE>", language)