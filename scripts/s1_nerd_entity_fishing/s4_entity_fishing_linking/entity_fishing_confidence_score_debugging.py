# %%

import json

import requests as r

import sys
from os import path

from requests.api import request
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle, stream_to_jsonl

from s1_nerd_entity_fishing.s2_entity_fishing_evaluation.s0_sample_dhs_articles_for_evaluation import sampled_articles_by_language
from data_file_paths import S4_ENTITY_FISHING_LINKING_TEST_DATA_FOLDER, localize
# %%

debugging_jsonl = path.join(S4_ENTITY_FISHING_LINKING_TEST_DATA_FOLDER, "linked-dhs-<LANGUAGE>-confidence-score-debugging.jsonl")

# LINKING AND STREAMING LINKED ARTICLES TO JSONL
lng="fr"
articles10 = [a for a in sampled_articles_by_language[lng][0:10]]

stream_to_jsonl(
    localize(debugging_jsonl,lng),
    dhs_article.link_dhs_articles(articles10, include_entities=False),
    drop_page_content=True
)


awk = [(a.title, a.wikidata_url, a.wikipedia_page_title) for a in articles10]


# %% LOADING BACK LINKED ARTICLES

new_articles = list(DhsArticle.load_articles_from_jsonl(localize(debugging_jsonl,lng)))

[sum(len(tls) for tls in a.text_links) for a in new_articles]
[a.title for a in new_articles]

# %%

article = articles10[1]

document = dhs_article.document_from_dhs_article(article)

# %%


# %% sending query by hand

json_query = entity_fishing.document_to_json_request(document, "fr", False, as_dict=True)


entity_fishing_base_url = "http://localhost:8090"
entity_fishing_disambiguate_path = "/service/disambiguate"
entity_fishing_disambiguate_url = entity_fishing_base_url+entity_fishing_disambiguate_path



entity_fishing_resp = r.post(entity_fishing_disambiguate_url, json = json_query)

result = json.loads(entity_fishing_resp.content)
result
# %%

augmented_document = entity_fishing.document_augment_from_json_response(document, result)
# %%

"""
bug found:

```
class Annotation:
    def __init__(
            self,
            start,
            ...
            extra_fields=dict()
        )
        ...
        self.extra_fields = extra_fields
```
-> means all instances of Annotation have extra_fields pointing to the same dict

correction (also done for Document):
```
class Annotation:
    def __init__(
            ...
            extra_fields=None
        ):
        ...
        self.extra_fields:dict = extra_fields if extra_fields is not None else dict()
```

"""
# %%
