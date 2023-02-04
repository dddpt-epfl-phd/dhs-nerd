import pandas as pd
from spacy import displacy
from spacy.tokens import Doc
from spacy.vocab import Vocab
from spacy_streamlit.util import get_html
import streamlit as st
import torch
from transformers import BertTokenizerFast


from transformers import AutoModel

@st.cache(allow_output_mutation=True)
def load_model():
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')
    model = AutoModel.from_pretrained(
            "QCRI/PropagandaTechniquesAnalysis-en-BERT",
             revision="v0.1.0")
    return tokenizer, model
    
tokenizer, model = load_model()

st.write("[Propaganda Techniques Analysis BERT](https://huggingface.co/QCRI/PropagandaTechniquesAnalysis-en-BERT) Tagger")

input = st.text_area('Input', """\
In some instances, it can be highly dangerous to use a medicine for the prevention or treatment of COVID-19 that has not been approved by or has not received emergency use authorization from the FDA.
""")

inputs = tokenizer.encode_plus(input, return_tensors="pt")
outputs = model(**inputs)
sequence_class_index = torch.argmax(outputs.sequence_logits, dim=-1)
sequence_class = model.sequence_tags[sequence_class_index[0]]
token_class_index = torch.argmax(outputs.token_logits, dim=-1)
tokens = tokenizer.convert_ids_to_tokens(inputs.input_ids[0][1:-1])
tags = [model.token_tags[i] for i in token_class_index[0].tolist()[1:-1]]

spaces = [not tok.startswith('##') for tok in tokens][1:] + [False]

doc = Doc(Vocab(strings=set(tokens)),
          words=tokens,
          spaces=spaces,
          ents=[tag if tag == "O" else f"I-{tag}" for tag in tags])

print("tags:")
print(tags)
labels = TOKEN_TAGS[2:]

label_select = st.multiselect(
    "Tags",
    options=labels,
    default=labels,
    key=f"tags_ner_label_select",
)
html = displacy.render(
    doc, style="ent", options={"ents": label_select, "colors": {}}
)
style = "<style>mark.entity { display: inline-block }</style>"
st.write(f"{style}{get_html(html)}", unsafe_allow_html=True)

attrs = ["text", "label_", "start", "end", "start_char", "end_char"]
data = [
    [str(getattr(ent, attr)) for attr in attrs]
    for ent in doc.ents
    if ent.label_ in label_select
]
if data:
    df = pd.DataFrame(data, columns=attrs)
    st.dataframe(df)
