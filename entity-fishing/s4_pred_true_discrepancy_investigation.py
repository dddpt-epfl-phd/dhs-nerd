# %%
import spacy

from inception_fishing import Corpus, Document, Annotation


from s1_from_entity_fishing_to_inception import predicted_corpora_by_lng
from s2_from_inception_annotation_to_entity_fishing import annotated_corpora_by_lng
from utils import spacy_models_by_lng

# %%
language = "de"

pred_corpus:Corpus = predicted_corpora_by_lng[language]
true_corpus:Corpus = annotated_corpora_by_lng[language]

pred_doc = pred_corpus.documents[0]


# %%
for pred_doc in pred_corpus.documents:
    print(f"Cheking tokens are the same in pred_ and true_ for document {pred_doc.name}")

    nlp = spacy.load(spacy_models_by_lng[language])

    true_doc = [d for d in true_corpus.documents if d.name==pred_doc.name][0]

    pred_doc_spacy = pred_doc.spacy_to_doc(nlp)
    true_doc_spacy = true_doc.spacy_to_doc(nlp)

    pred_tokens = [t for t in pred_doc_spacy]
    true_tokens = [t for t in true_doc_spacy]

    for i,t in enumerate(pred_tokens):
        if t.text!= true_tokens[i].text:
            print(f'pred_token({t.text}, idx={t.idx}, len={len(t)}))\t\ttrue_token({true_tokens[i].text}, idx={true_tokens[i].idx}, len={len(true_tokens[i])}))')
        assert t.text== true_tokens[i].text

    
    if true_doc.text!= pred_doc.text:
        print(f'Document different between pred_ and true_ for doc {pred_doc.name}')
        assert true_doc.text== pred_doc.text
    else:
        print(f'Document text checked and identical for doc {pred_doc.name}')
        
# %% Danube mistake:

danube_pred_doc = [d for d in pred_corpus.documents if d.name=="Danube.fr.txt"][0]
danube_true_doc = [d for d in true_corpus.documents if d.name=="Danube.fr.txt"][0]

# %%
