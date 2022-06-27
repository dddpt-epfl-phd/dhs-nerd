
# %%
from cassis import *

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from polities_to_extract_rules import *
from data_file_paths import S0_JSONL_ALL_ARTICLES_PARSED_FILE, localize

# %%


language="fr"

articles = get_articles(language)
articles_by_category = get_articles_by_category(articles)
spatial_articles = articles_by_category["spatial"]

polities_dtf = get_polities_to_extract_dtf(spatial_articles=spatial_articles)
polities_dtf.head()

# %%




