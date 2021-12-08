# %%
import spacy
import pandas as pd

from inception_fishing import Corpus, Document, Annotation

from s2_entity_fishing_evaluation.s2_from_entity_fishing_to_inception import predicted_corpora_by_lng
from s2_entity_fishing_evaluation.s3_prepare_evaluation import annotated_corpora_by_lng
from s2_entity_fishing_evaluation.s5_scoring_only_dhs_entities import dhs_only_corpora_by_lng, dhs_wk_only_corpora_by_lng 
from utils import spacy_models_by_lng

# %%
language = "de"

pred_corpus:Corpus = predicted_corpora_by_lng[language]
true_corpus:Corpus = annotated_corpora_by_lng[language]

pred_doc = pred_corpus.documents[0]


# %% Investigating spacy tokenization discrepancies induced by inception

if False:
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
        
    # Danube mistake:

    danube_pred_doc = [d for d in pred_corpus.documents if d.name=="Danube.fr.txt"][0]
    danube_true_doc = [d for d in true_corpus.documents if d.name=="Danube.fr.txt"][0]



# %% Investigating grobid class of wd entities in DHS & WK

language = "fr"

dhs_only_pred_corpus:Corpus = dhs_only_corpora_by_lng[language][0]
dhs_only_true_corpus:Corpus = dhs_only_corpora_by_lng[language][1]

dhs_only_annotations = [a for d in dhs_only_true_corpus.documents for a in d.annotations]

pd_dhs_only_annotations = pd.DataFrame({
    "start": [a.start for a in dhs_only_annotations],
    "end": [a.end for a in dhs_only_annotations],
    "wikidata_entity_id": [a.wikidata_entity_id for a in dhs_only_annotations],
    "wikipedia_page_id": [a.wikipedia_page_id for a in dhs_only_annotations],
    "wikipedia_page_title": [a.wikipedia_page_title for a in dhs_only_annotations],
    #"wikidata_entity_url": [a.wikidata_entity_url for a in dhs_only_annotations],
    "mention": [a.mention for a in dhs_only_annotations],
    "grobid_tag": [a.grobid_tag for a in dhs_only_annotations],
})



# %%
