# %%


import json
from os import path
from random import randint, seed

import requests as r

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")

from dhs_scraper import DhsArticle, TOTAL_NB_DHS_ARTICLES, stream_to_jsonl
from data_file_paths import S0_JSONL_ALL_ARTICLES_NO_PAGE_FILE, S0_JSONL_ALL_ARTICLES_FILE, S2_INCEPTION_SAMPLED_ARTICLES_IDS, S2_ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER, S2_INCEPTION_SAMPLED_ARTICLES, localize

seed(54321)

sampling_language="de" # determines from which language corpus we'll chose article to load


sampled_languages = ["de", "fr"]

if __name__ =="__main__":
    print("ENTERING MAIN")

    # %% Sample articles
    nb_articles_sampled = 50

    articles_indices = set()
    for i in range(nb_articles_sampled):
        random_index = randint(0, TOTAL_NB_DHS_ARTICLES)
        if random_index not in articles_indices:
            articles_indices.add(random_index)

    # %%

    all_ids = list(DhsArticle.get_articles_ids(localize(S0_JSONL_ALL_ARTICLES_NO_PAGE_FILE, sampling_language)))

    new_articles_ids = [all_ids[i] for i in articles_indices]

    # %% Write text to corresponding RawText folder

    sampled_articles_by_language = {
        lng: [a for a in DhsArticle.load_articles_from_jsonl(localize(S0_JSONL_ALL_ARTICLES_FILE, lng),new_articles_ids)] 
        for lng in sampled_languages   
    }

    sampled_articles_ids_json = [
        (a.id, a.title) 
        for a in sampled_articles_by_language["fr"]
    ]

    for lng, articles in sampled_articles_by_language.items():
        with open(localize(S2_INCEPTION_SAMPLED_ARTICLES, lng), "w") as f:
            f.write("")
        stream_to_jsonl(localize(S2_INCEPTION_SAMPLED_ARTICLES, lng), articles)

    with open(S2_INCEPTION_SAMPLED_ARTICLES_IDS, "w") as sampled_json:
        json.dump(sampled_articles_ids_json, sampled_json)



# if not the main script, simply load the sampled articles from jsonls
else:
    # %%
    sampled_articles_by_language = {
        lng: list(DhsArticle.load_articles_from_jsonl(localize(S2_INCEPTION_SAMPLED_ARTICLES, lng)))
        for lng in sampled_languages
    }

# %%

# %% Sending a query to entity-fishing service on 8090
# needs access to running entity-fishing service on entity_fishing_url (by default: localhost:8090)

if False:

    entity_fishing_base_url = "http://localhost:8090"
    entity_fishing_disambiguate_path = "/service/disambiguate"

    query = {
        "text": "Seigneurie du XIe s. ?? 1475, bailliage commun de Berne et Fribourg jusqu'en 1798, distr. vaudois depuis 1798. La grande seigneurie de Grandson, domaine de la famille du m??me nom, s'??tendait sur tout le pied du Jura vaudois; Montricher en fut d??tach?? avant 1049 et Belmont en 1185. Au d??but du XIIe s., Ebal Ier para??t avoir fix?? sa r??sidence ?? La Sarraz. Avant 1234, Ebal IV partagea la seigneurie en trois, La Sarraz, Champvent et Grandson, celle-ci revenant ?? son fils cadet, Pierre Ier. Ch??telains seigneuriaux, les Grandson avaient des attributions militaires et financi??res plus ??tendues que les ch??telains des Savoie; ils exerc??rent jusqu'en 1381 la charge honorifique de vidomne d'Yverdon. A la suite de la condamnation d'Hugues pour faux en 1389, la ch??tellenie fut confisqu??e par le comte de Savoie et inf??od??e en 1400 ?? Marguerite de Montb??liard, puis en 1424 ?? Louis de Chalon. A sa mort en 1463, ses fils Guillaume et Hugues se disput??rent ses possessions; d??bout?? par la Savoie, Guillaume fit appel ?? l'empereur Fr??d??ric III; l'??v??que de Constance, commis juge unique, annula le jugement. Mais les Chalon furent d??pouill??s en 1475-1476 par les Suisses lors des guerres de Bourgogne. La seigneurie de Grandson fut attribu??e aux Conf??d??r??s et, avec la terre de Montagny, forma d??s 1484 un bailliage commun de Berne et Fribourg. Chacun des deux cantons nommait ?? tour de r??le un bailli pour cinq ans, les appels ??tant port??s vers le souverain d'alternative, celui dont le bailli n'??tait pas ressortissant. En 1531, les premiers partisans de la R??forme obtinrent l'envoi d'un pr??dicant; les deux cantons convinrent que les r??form??s pourraient pratiquer leur culte et demander que l'on proc??de dans chaque paroisse au Plus, vote pour d??cider de la confession. La r??sistance de Fribourg, qu'un partage des biens de la chartreuse de La Lance pouvait tenter, ne fut pas tr??s forte et la R??forme l'emporta partout, entre 1531 (Fiez) et 1564 (Bonvillars). L'organisation judiciaire comprenait treize cours de justice, l'une en ville de Grandson, si??ge de la ch??tellenie, les autres dans les cinq m??tralies (Bonvillars, Concise, Fiez, Provence et Yvonand), les quatre territoires inf??od??s (Corcelles, Chamblon, Essert et Valeyres), la terre de Montagny, la mairie d'Onnens et ?? Vuiteboeuf, qui relevait du bailliage pour un tiers. Le tribunal baillival et la cour criminelle si??geaient ?? Grandson; enfin, Grandson et les quatre fiefs avaient leur cour des fiefs et les huit paroisses dix consistoires. On appliqua le coutumier de Grandson (1702) jusqu'?? l'introduction du Code de proc??dure civile vaudois en 1825. La plupart de ses 442 articles ??taient repris du droit de Moudon de 1577. Le bailliage, financi??rement de deuxi??me classe, abritait des foires ?? Grandson, Concise, Champagne et Provence; l'exploitation des for??ts ??tait l'industrie principale. En 1798, le bailliage fut peu favorable ?? la r??volution; des insurg??s march??rent sur Yverdon et furent d??faits le 4 mars ?? Vuiteboeuf; en outre, plusieurs dizaines d'hommes rejoignirent la L??gion fid??le. En 1798, le district de Grandson fut form?? de l'ancien bailliage (moins Chamblon, Essert, Montagny, Villars-sous-Champvent et Yvonand, r??unis ?? celui d'Yverdon), de Sainte-Croix et Bullet, ainsi que, jusqu'en 1803, de Baulmes, Vuiteboeuf, Vugelles-la-Mothe et Valeyres-sous-Montagny. En 1798, le bailliage comptait 5955 habitants (8324 pour le district actuel, 5,8% de la population vaudoise). La population a peu augment?? (10 695 hab. en 1850, 13 550 en 1900, 12 816 en 1950 et 12 253 en 2000, 1,9% de la population vaudoise) voire a baiss?? ?? la fin du XXe s. (exode rural et crise industrielle ?? Sainte-Croix). Divis?? en trois cercles de justice de paix (Grandson, Concise et Sainte-Croix), le district a eu deux pr??fectures, Grandson et Sainte-Croix, jusqu'?? la suppression de la seconde en 1949.",
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