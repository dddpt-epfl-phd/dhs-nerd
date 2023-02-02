
# %%
import json

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

from spacy.tokens import Doc
from spacy.vocab import Vocab
from spacy import displacy

#%%

sys.path.append("../../../src")
sys.path.append("../../../scripts")
from inception_fishing import Annotation

from data_file_paths import *
from s2_nerd.s0_spatial_articles.s2_prepare_articles import *
from s2_nerd.s0_spatial_articles.spatial_articles_utils import *

# %%



additional_columns = [
    "article", "document"]
articles_dtf = get_articles_dtf_from_polities_dtf(polities_dtf, additional_columns)
sampled_articles_dtf = articles_dtf[articles_dtf.hds_article_id.apply(lambda id: id in sampled_articles_ids)].copy()

sampled_articles_dtf["text_len"] = sampled_articles_dtf.document.apply(lambda d: len(d.text))
#sampled_articles_dtf.document.apply(lambda d: tokenizer(normalize_unicode_text(d.text)))
sampled_articles_dtf.sort_values(by="text_len", inplace=True)

# %%


# %%

# %%

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# %%

#model = AutoModel.from_pretrained(checkpoint)
model = AutoModelForTokenClassification.from_pretrained(checkpoint)
# %%


ner_pipeline = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# %%

def article_entity_recognition(dhs_article, pipeline):
    """
    Algo:
    - do the NER per text_block
    - per text_block:
        - create tokens based on ner_results
    """
    tb_ner_results = [
        pipeline(text)
        for tag, text in dhs_article.text_blocks
    ]
    # handle float32s for json dumping
    for ner_results in tb_ner_results:
        for nr in ner_results:
            nr["score"] = float(nr["score"])
    return tb_ner_results


def json_dump_huggingface_ner_results(dhs_article, dhsa_ner_results, jsonfile="huggingface_ner_results.json"):
    with open(jsonfile, "w") as nerf:
        json.dump({
            "hds_article_id": dhs_article.id,
            "text_blocks": dhs_article.text_blocks,
            "ner_results": dhsa_ner_results
        }, nerf, indent="\t", ensure_ascii=False)


def displacy_article_ner_results(text_blocks, tb_ner_results, included_ents=["LOC", "DATE", "PER"]):
    """
    Algo:
    - per text block:
        - compute fake tokens from ner_results
    """
    tokens = []
    ents = []
    for i, (tag,tb) in enumerate(text_blocks):
        ner_results = tb_ner_results[i]
        for i, nr in enumerate(ner_results):
            if i!=0:
                prev_nr = ner_results[i-1]
                if nr["start"] > prev_nr["end"] :
                    tokens.append(tb[prev_nr["end"]:nr["start"]])
                    ents.append("O")
            tokens.append(tb[nr["start"]:nr["end"]])
            if nr["entity_group"] in included_ents:
                ents.append("B-"+nr["entity_group"])
            else:
                ents.append("O")
    return tokens, ents

def displacy_dhs_article_NER(dhs_article, dhsa_ner_results):
    tokens, ents = displacy_article_ner_results(dhs_article.text_blocks, dhsa_ner_results)
    doc = Doc(Vocab(strings=set(tokens)),
            words=tokens,
            # spaces=spaces,
            ents=ents
    )
    return displacy.render(doc, style="ent")
# %%

# %%

# %%
dhs_article = sampled_articles_dtf.article.iloc[22]
dhsa_ner_results = article_entity_recognition(dhs_article, ner_pipeline)

tokens, ents =  displacy_article_ner_results(dhs_article.text_blocks, dhsa_ner_results)
displacy_dhs_article_NER(dhs_article, dhsa_ner_results)
# %%
# %%
json_dump_huggingface_ner_results(dhs_article, dhsa_ner_results, jsonfile="huggingface_ner_results.json")



# %%

sampled_articles_dtf["ner_results"] = sampled_articles_dtf.article.apply(lambda a: article_entity_recognition(a, ner_pipeline))

# %%

i = 39
dhs_article = sampled_articles_dtf.article.iloc[i]
dhsa_ner_results = sampled_articles_dtf.ner_results.iloc[i]
print(dhs_article.id)
displacy_dhs_article_NER(dhs_article, dhsa_ner_results)

# %%
