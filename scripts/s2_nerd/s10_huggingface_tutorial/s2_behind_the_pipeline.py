
# %%
from transformers import AutoTokenizer
from transformers import AutoModel

# %%
#checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
checkpoint = "Jean-Baptiste/camembert-ner-with-dates"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# %%
raw_inputs = [
    "En 1324, la seigneurie justicière passa de Heinrich von Wespersbühl à Walter von Gachnang et, en 1377, aux Hohenlandenberg."
    "T. échut en 1434 à Zurich avec la seigneurie d'Andelfingen. Une chapelle Saint-Martin, filiale d'Andelfingen, mentionnée en 1370, fut rénovée en 1489.",
]
inputs = tokenizer(raw_inputs, padding=True, truncation=True, return_tensors="pt")
print(inputs)
# %%

model = AutoModel.from_pretrained(checkpoint)
# %%

outputs = model(**inputs)
print(outputs.last_hidden_state.shape)
# %%
from transformers import AutoModelForSequenceClassification

#checkpoint = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)
outputs = model(**inputs)
# %%

print(outputs.logits.shape)
print(outputs.logits)
# %%

import torch

predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
print(predictions)
# %%
