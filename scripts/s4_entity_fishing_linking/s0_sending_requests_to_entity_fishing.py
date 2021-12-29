# %%


import sys

sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import dhs_article
from dhs_scraper import DhsArticle, stream_to_jsonl

from data_file_paths import S0_JSONL_ALL_ARTICLES_FILE, S4_JSONL_ALL_ARTICLES_LINKED_FILE, S4_ENTITY_FISHING_TIMED_OUT_ARTICLES_FILE, localize
# %%
"""
This scripts load all the DhsArticles in S0_JSONL_ALL_ARTICLES_FILE, links them with entity-fishing and streams them back into a json in S4_JSONL_ALL_ARTICLES_LINKED_FILE

usage from this folder:
```
python s0_sending_requests_to_entity_fishing.py >> ../../data/entity-fishing-linking/logs/linking-LNG-DATE 2>> ../../data/entity-fishing-linking/logs/linking-LNG-DATE-stderr
```


Todo
1) DONE re-integration of doc.annotations in dhs_article.text_links
2) DONE test & ensure DhsA to jsonl works correctly with both text_content and text_links
3) DONE write code for whole of step 1) DhsA through EF
4) create mDhsA data-structure
5) write code for step 2) Unify DhsAs into mDhsAs
"""

# LINKING AND STREAMING LINKED ARTICLES TO JSONL
default_language="it"
entity_fishing_timeout = None

language = default_language
possible_languages = ["fr", "de", "it"]
if len(sys.argv)>1:
    if sys.argv[1] in possible_languages:
        language = sys.argv[1]
    else:
        raise Exception(f"s0_scrape.py: unrecognized language argument from sys.argv[1]: '{sys.argv[1]}'. Must be one of {possible_languages}")


jsonl_linked_articles_file = localize(S4_JSONL_ALL_ARTICLES_LINKED_FILE, language)
already_visited_ids = set(DhsArticle.get_articles_ids(jsonl_linked_articles_file))
bugged_ids = {
    "de": [
        "012199", "012463", "029202", "012509", "058090", "041455", "020785", "020786",
        "020787", "020589", "020590", "011635", "020772", "012584", "012583", "020793",
        "012614", "029215", "029199", "029200", "029209", "012635", "029219", "029217",
        "029210", "046529", "019681"
    ],
    "fr": [
        "058089", "058090", "044498", "031336", "048634", "048313", "044235", "027390",
        "049777"
    ]
}
#for bugged_id in bugged_ids[language]:
#    already_visited_ids.add(bugged_id)
print(f"Skipping {len(already_visited_ids)} articles that already have been linked")
stream_to_jsonl(
    jsonl_linked_articles_file,
    dhs_article.link_dhs_articles(
        DhsArticle.load_articles_from_jsonl(
            localize(S0_JSONL_ALL_ARTICLES_FILE,language),
            ids_to_drop=already_visited_ids
        ),
        entity_fishing_timeout = entity_fishing_timeout,
        timed_out_articles_file = localize(S4_ENTITY_FISHING_TIMED_OUT_ARTICLES_FILE, language),
        include_entities=False
    ),
    buffer_size=10,
    drop_page_content=True
)


# %%

# %%
