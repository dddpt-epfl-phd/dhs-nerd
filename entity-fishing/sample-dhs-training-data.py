# %%


import json
from os import path
from random import randint, seed

import requests as r

from dhs_scraper import DhsArticle, TOTAL_NB_DHS_ARTICLES
from utils import DHS_DUMP_JSONL_FILE, get_dhs_dump_jsonl_file

seed(54321)

sampling_language="de" # determines from which language corpus we'll chose article to load

ARTICLES_SAMPLE_DIRECTORY = f"entity-fishing/data/corpus/corpus-long/dhs-training-<LANGUAGE>/RawText/"

sampled_languages = ["de", "fr"]

# %% Sample articles (stupid way, but keep it to maintain same sample as already annotated in inception)

nb_articles_sampled = 50

articles_indices = set()
for i in range(nb_articles_sampled):
    random_index = randint(0, TOTAL_NB_DHS_ARTICLES)
    if random_index not in articles_indices:
        articles_indices.add(random_index)

# %%

all_ids = list(DhsArticle.get_articles_ids(get_dhs_dump_jsonl_file(sampling_language)))

new_articles_ids = [all_ids[i] for i in articles_indices]

# %% Write text to corresponding RawText folder

for lng in sampled_languages:
    print(f"\n\nSampling articles for language {lng}\n=========================================")
    for a in DhsArticle.load_articles_from_jsonl(get_dhs_dump_jsonl_file(lng),articles_ids):
        with open(path.join(ARTICLES_SAMPLE_DIRECTORY.replace("<LANGUAGE>", lng),a.title+f".{lng}.txt"), "w") as rawtext_file:
            print(f"writing for article {a.title}")
            rawtext_file.write(a.text)



# %% Sending a query to entity-fishing service on 8090
# needs access to running entity-fishing service on entity_fishing_url (by default: localhost:8090)

if False:

    entity_fishing_base_url = "http://localhost:8090"
    entity_fishing_disambiguate_path = "/service/disambiguate"

    query = {
            "text": "Seigneurie du XIe s. à 1475, bailliage commun de Berne et Fribourg jusqu'en 1798, distr. vaudois depuis 1798. La grande seigneurie de Grandson, domaine de la famille du même nom, s'étendait sur tout le pied du Jura vaudois; Montricher en fut détaché avant 1049 et Belmont en 1185. Au début du XIIe s., Ebal Ier paraît avoir fixé sa résidence à La Sarraz. Avant 1234, Ebal IV partagea la seigneurie en trois, La Sarraz, Champvent et Grandson, celle-ci revenant à son fils cadet, Pierre Ier. Châtelains seigneuriaux, les Grandson avaient des attributions militaires et financières plus étendues que les châtelains des Savoie; ils exercèrent jusqu'en 1381 la charge honorifique de vidomne d'Yverdon. A la suite de la condamnation d'Hugues pour faux en 1389, la châtellenie fut confisquée par le comte de Savoie et inféodée en 1400 à Marguerite de Montbéliard, puis en 1424 à Louis de Chalon. A sa mort en 1463, ses fils Guillaume et Hugues se disputèrent ses possessions; débouté par la Savoie, Guillaume fit appel à l'empereur Frédéric III; l'évêque de Constance, commis juge unique, annula le jugement. Mais les Chalon furent dépouillés en 1475-1476 par les Suisses lors des guerres de Bourgogne. La seigneurie de Grandson fut attribuée aux Confédérés et, avec la terre de Montagny, forma dès 1484 un bailliage commun de Berne et Fribourg. Chacun des deux cantons nommait à tour de rôle un bailli pour cinq ans, les appels étant portés vers le souverain d'alternative, celui dont le bailli n'était pas ressortissant. En 1531, les premiers partisans de la Réforme obtinrent l'envoi d'un prédicant; les deux cantons convinrent que les réformés pourraient pratiquer leur culte et demander que l'on procède dans chaque paroisse au Plus, vote pour décider de la confession. La résistance de Fribourg, qu'un partage des biens de la chartreuse de La Lance pouvait tenter, ne fut pas très forte et la Réforme l'emporta partout, entre 1531 (Fiez) et 1564 (Bonvillars). L'organisation judiciaire comprenait treize cours de justice, l'une en ville de Grandson, siège de la châtellenie, les autres dans les cinq métralies (Bonvillars, Concise, Fiez, Provence et Yvonand), les quatre territoires inféodés (Corcelles, Chamblon, Essert et Valeyres), la terre de Montagny, la mairie d'Onnens et à Vuiteboeuf, qui relevait du bailliage pour un tiers. Le tribunal baillival et la cour criminelle siégeaient à Grandson; enfin, Grandson et les quatre fiefs avaient leur cour des fiefs et les huit paroisses dix consistoires. On appliqua le coutumier de Grandson (1702) jusqu'à l'introduction du Code de procédure civile vaudois en 1825. La plupart de ses 442 articles étaient repris du droit de Moudon de 1577. Le bailliage, financièrement de deuxième classe, abritait des foires à Grandson, Concise, Champagne et Provence; l'exploitation des forêts était l'industrie principale. En 1798, le bailliage fut peu favorable à la révolution; des insurgés marchèrent sur Yverdon et furent défaits le 4 mars à Vuiteboeuf; en outre, plusieurs dizaines d'hommes rejoignirent la Légion fidèle. En 1798, le district de Grandson fut formé de l'ancien bailliage (moins Chamblon, Essert, Montagny, Villars-sous-Champvent et Yvonand, réunis à celui d'Yverdon), de Sainte-Croix et Bullet, ainsi que, jusqu'en 1803, de Baulmes, Vuiteboeuf, Vugelles-la-Mothe et Valeyres-sous-Montagny. En 1798, le bailliage comptait 5955 habitants (8324 pour le district actuel, 5,8% de la population vaudoise). La population a peu augmenté (10 695 hab. en 1850, 13 550 en 1900, 12 816 en 1950 et 12 253 en 2000, 1,9% de la population vaudoise) voire a baissé à la fin du XXe s. (exode rural et crise industrielle à Sainte-Croix). Divisé en trois cercles de justice de paix (Grandson, Concise et Sainte-Croix), le district a eu deux préfectures, Grandson et Sainte-Croix, jusqu'à la suppression de la seconde en 1949.",
            "shortText": "",
            "termVector": [],
            "language": {
                "lang": "fr"
            },
            "entities": [],
            "mentions": [
                "ner",
                "wikipedia"
            ],
            "nbest": 5,
            "sentence": False
        }

    resp = r.post(entity_fishing_base_url+entity_fishing_disambiguate_path, json = query)
    entities = resp.json()

    with open("test_resp.json", "w") as f:
        json.dump(entities, f, ensure_ascii=False)