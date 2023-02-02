
# %%
import json

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

import torch
import numpy as np

#%%

sys.path.append("../../../src")
sys.path.append("../../../scripts")
from inception_fishing import Annotation

from s2_nerd.s0_spatial_articles.s2_prepare_articles import *
from s2_nerd.s0_spatial_articles.spatial_articles_utils import *
import spacy
from tqdm import tqdm

# %%



additional_columns = [
    "article", "document"]
articles_dtf = get_articles_dtf_from_polities_dtf(polities_dtf, additional_columns)
sampled_articles_dtf = articles_dtf[articles_dtf.hds_article_id.apply(lambda id: id in sampled_articles_ids)].copy()

sampled_articles_dtf["text_len"] = sampled_articles_dtf.document.apply(lambda d: len(d.text))
#sampled_articles_dtf.document.apply(lambda d: tokenizer(normalize_unicode_text(d.text)))
sampled_articles_dtf.sort_values(by="text_len", inplace=True)

# %%


spacy_tokenizer = spacy.load("fr_core_news_sm")

# %%
add_tokenized_text(sampled_articles_dtf, spacy_tokenizer)
# %%
raw_inputs = [
    "En 1324, la seigneurie justicière passa de Heinrich von Wespersbühl à Walter von Gachnang et, en 1377, aux Hohenlandenberg."
    "T. échut en 1434 à Zurich avec la seigneurie d'Andelfingen. Une chapelle Saint-Martin, filiale d'Andelfingen, mentionnée en 1370, fut rénovée en 1489.",
]
# %%
indices = range(96,100)
raw_inputs = list(sampled_articles_dtf.iloc[indices].document.apply(lambda d: d.text))

# %%


sampled_articles_dtf.iloc[indices].tokens.apply(len)

# %%

# %%
#checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
checkpoint = "Jean-Baptiste/camembert-ner-with-dates"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# %%

# max_length for camemBERT is 512 tokens
inputs = tokenizer(raw_inputs, padding="max_length", truncation=True, return_tensors="pt")


# %%
#tokenzz = [tokenizer.decode(id, skip_special_tokens=True) for id in inputs.input_ids[0]]
tokens_text = [tokenizer.decode(id, skip_special_tokens=True) for ids in inputs.input_ids for id in ids]
tokens_text
# %%
tokens = [tokenizer.convert_ids_to_tokens(ids, skip_special_tokens=True) for ids in inputs.input_ids]
tokens
# %%
tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0], skip_special_tokens=True)
# tokens[0].start
# %%
# ! important: decoded text doesn't include line returns!!
decoded_text_from_tokens = tokenizer.convert_tokens_to_string(tokens)
decoded_text_from_input_ids = tokenizer.decode(inputs.input_ids[0], skip_special_tokens=True)
decoded_text_from_input_ids

# %%

print(inputs.input_ids.shape)
# %%


#model = AutoModel.from_pretrained(checkpoint)
model = AutoModelForTokenClassification.from_pretrained(checkpoint)
# %%

outputs = model(**inputs)
# %%
print(outputs.logits.shape)

# %%
# %%
# %%


predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions.shape)
# %%

predictions[0][32].detach().numpy().round(3)

# %%
model
# %%


camembert_ner = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# %%
text = sampled_articles_dtf.article.iloc[99].text_blocks[33][1]

ner_results = camembert_ner(
    text
)
ner_results
 # %%
for r in ner_results:
    r["score"] = float(r["score"])

# %%


# %%
def json_dump_huggingface_ner_results(text, ner_results, jsonfile="huggingface_ner_results.json"):
    with open(jsonfile, "w") as nerf:
        json.dump({"text":text, "ner_results":ner_results}, nerf, indent="\t", ensure_ascii=False)

# %%
json_dump_huggingface_ner_results(text, ner_results, jsonfile="huggingface_ner_results.json")
# %%

def tokens_ner_to_displacy_labels(tokens_texts, ner_results):
    """
    Algo
    - loop over the tokens
        - compute start + end of current_token
        - compute current_ner_result based on those limits
        - if current token in ner_result set up label
        - if current_ner_result out, jump out of it.
    """
    ents = []
    token_start = 0
    token_end = 0
    current_ner_result_index = 0
    current_ner_result = ner_results[current_ner_result_index]
    for token in tokens_texts:
        token_start = token_end
        token_end = token_start+len(token)
        if token_start>= current_ner_result["start"] and token_end<= current_ner_result["end"]:
            ents.append(current_ner_result["entity_group"])
        elif token_start>= current_ner_result["start"] and token_end>= current_ner_result["end"]:
            print(f"PROBLEM OVERLAPPING TOKENS token_start={token_start}, token_end={token_end}")
            print(f'\tcurrent_ner_result["start"]={current_ner_result["start"]}, current_ner_result["end"]={current_ner_result["end"]}')
        else:
            ents.append("O")
        if token_start >=current_ner_result["end"]:
            current_ner_result_index +=1
            current_ner_result = ner_results[current_ner_result_index]
    return ents

# %%

ner_ents = tokens_ner_to_displacy_labels(tokens_text, ner_results)
# %%
ner_results

# %%

# HF+DISPLACY TEST

from spacy.tokens import Doc
from spacy.vocab import Vocab
from spacy import displacy

ents_mockup = ["O", "O", "O", "O", "I-LOC", "O", "O", "I-PER", "O", "I-LOC"]
ds_tokens = [t for t in tokens_text if len(t)>0]
ents = [ents_mockup[i %len(ents_mockup)] for i,t in enumerate(ds_tokens)]
ents
# %%

doc = Doc(Vocab(strings=set(ds_tokens)),
        words=ds_tokens,
        # spaces=spaces,
        ents=ents
)
displacy.render(doc, style="ent")

# %%

# overkill at the moment: simply pass text+identified entities
if False:
    def hf_tokens_to_json_tokens(tokens_str):
        pass

    # %%


    def text_to_json_tokens(tokenizer, input_ids=None, text=None):
        if input_ids is None and text is None:
            raise("Error: text_to_json_tokens() expects at least one of input_ids or text to be not None")
        if input_ids is None:
            input_ids = tokenizer(text, padding="max_length", truncation=True, return_tensors="pt").input_ids[0]

        #tokenzz = [tokenizer.decode(id, skip_special_tokens=True) for id in inputs.input_ids[0]]
        tokens_text = [tokenizer.decode(id, skip_special_tokens=True) for ids in inputs.input_ids for id in ids]
        tokens_text


    def predictions_to_to_json_tokens():
        pass 
# %%
