# %%

import json

import requests as r

import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from inception_fishing import entity_fishing, dhs_article, wikipedia
from dhs_scraper import DhsArticle

from s2_entity_fishing_evaluation.s0_sample_dhs_articles_for_evaluation import sampled_articles_by_language

# %%

article = sampled_articles_by_language["fr"][0]
document = dhs_article.document_from_dhs_article(article)


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

nerd_doc = entity_fishing.document_named_entity_linking(document, "fr")

nerda = [a for a in nerd_doc.annotations if a.extra_fields.get("origin")=="entity_fishing"]
olda = [a for a in nerd_doc.annotations if a.extra_fields.get("origin")!="entity_fishing"]
olda
# %%

aventicum_doc2 = dhs_article.document_from_dhs_article(article)
nerd_doc2 = entity_fishing.document_named_entity_linking(aventicum_doc2, "fr", False)
nerda2 = [a for a in nerd_doc2.annotations if a.extra_fields.get("origin")=="entity_fishing"]

