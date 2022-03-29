# %%

import json

import requests as r

import sys

from requests.api import request
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle, stream_to_jsonl

from s2_entity_fishing_evaluation.s0_sample_dhs_articles_for_evaluation import sampled_articles_by_language
from data_file_paths import S4_JSONL_ENTITY_FISHING_LINKING_TEST_LINKED_DHSA, localize
# %%
"""



Needs:
- send at least DE+FR languages through EF
	-> output: documents
- put annotations from documents back into DhsArticle
- Unify DhsArticle of different languages into MultilingualDhsArticle (mDhsA)
- save each mDhsA into its own json
- mDhsA needs:
	- DhsA with annotations in their language, + urls

proposition:
1) DhsA through EF: iterate through DhsA.load_from_jsonl()
	-> get doc: dhs_article.document_from_dhs_article()
	-> send through EF: entity_fishing.document_named_entity_linking()
	-> add back annotations into DhsA.text_links
	-> remove DhsA.page_content
	-> save to new jsonl
2) Unify DhsAs into mDhsAs
	(-> create mDhsA data-structure)
	-> load all DhsA int mDhsA
	- output all mDhsA to their own json

Todo
1) re-integration of doc.annotations in dhs_article.text_links
2) test & ensure DhsA to jsonl works correctly with both text_content and text_links
3) write code for whole of step 1) DhsA through EF
4) create mDhsA data-structure
5) write code for step 2) Unify DhsAs into mDhsAs
"""

# LINKING AND STREAMING LINKED ARTICLES TO JSONL
lng="fr"
articles10 = [a for a in sampled_articles_by_language[lng][0:10]]

stream_to_jsonl(
    localize(S4_JSONL_ENTITY_FISHING_LINKING_TEST_LINKED_DHSA,lng),
    dhs_article.link_dhs_articles(articles10, include_entities=False),
    drop_page_content=True
)


awk = [(a.title, a.wikidata_url, a.wikipedia_page_title) for a in articles10]


# %% LOADING BACK LINKED ARTICLES

new_articles = list(DhsArticle.load_articles_from_jsonl(localize(S4_JSONL_ENTITY_FISHING_LINKING_TEST_LINKED_DHSA,lng)))

[sum(len(tls) for tls in a.text_links) for a in new_articles]
[a.title for a in new_articles]

# %%

article = sampled_articles_by_language["fr"][0]
article.parse_text_links()

article.add_wikidata_url_wikipedia_page_title()
article.add_wikidata_wikipedia_to_text_links()

document = dhs_article.document_from_dhs_article(article)

# %%


# %% sending query by hand

if False:
    json_query = entity_fishing.document_to_json_request(document, "fr", True)


    entity_fishing_base_url = "http://localhost:8090"
    entity_fishing_disambiguate_path = "/service/disambiguate"
    entity_fishing_disambiguate_url = entity_fishing_base_url+entity_fishing_disambiguate_path



    da = r.post(entity_fishing_disambiguate_url, json = json_query)

    result = json.loads(da.content)
    result
# %%

#result = entity_fishing.document_send_request(document, "fr")

# %%

wikipedia.document_set_annotations_page_titles_and_ids(document, "fr")
nerd_doc = entity_fishing.document_named_entity_linking(document, "fr")

nerda = [a for a in nerd_doc.annotations if a.extra_fields.get("origin")=="entity_fishing"]
olda = [a for a in nerd_doc.annotations if a.extra_fields.get("origin")!="entity_fishing"]
olda
# %%

aventicum_doc2 = dhs_article.document_from_dhs_article(article)
nerd_doc2 = entity_fishing.document_named_entity_linking(aventicum_doc2, "fr", False)
nerda2 = [a for a in nerd_doc2.annotations if a.extra_fields.get("origin")=="entity_fishing"]


tl1 = [tl for tls in article.text_links for tl in tls]
article2 = dhs_article.document_reintegrate_annotations_into_dhs_article(nerd_doc2, article)

tl2 = [tl for tls in article2.text_links for tl in tls]
# %%


# %%
