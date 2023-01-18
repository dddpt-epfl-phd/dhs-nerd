
# %%
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
camembert_ner(
    sampled_articles_dtf.article.iloc[99].text_blocks[33][1]
)

# %%
