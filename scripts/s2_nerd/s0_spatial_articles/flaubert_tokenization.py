
# %%

from transformers import  FlaubertTokenizer#, FlaubertModel


from s2_prepare_articles import *


# %%

flaubert_model='flaubert/flaubert_large_cased'
tokenizer = FlaubertTokenizer.from_pretrained(flaubert_model)

# %%
encoded_input = tokenizer(articles[0].text, return_tensors='pt') 
encoded_input2 = tokenizer.encode(articles[0].text) 

decoded_input = tokenizer.decode(encoded_input["input_ids"][0])
# %%

decoded_tokens = [tokenizer.decode(id) for id in encoded_input["input_ids"][0]]
# %%
