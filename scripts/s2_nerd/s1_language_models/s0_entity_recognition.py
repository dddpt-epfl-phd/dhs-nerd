
# %%
import json
import sys

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

spacy_tokenizer = spacy.load("fr_core_news_sm")
add_tokenized_text(sampled_articles_dtf, spacy_tokenizer)

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


def text_block_entity_recognition(text, pipeline, text_block_annotation=None):
    """Does the Named entity recognition for the given article, per text_blocks
    /!\ Some text_blocks are too long. As of now, they are truncated /!\
        
    """
    ner_results = pipeline(text)
        
    # handle float32s for json dumping
    for nr in ner_results:
        nr["score"] = float(nr["score"])
        if text_block_annotation is not None:
            nr["start"] = nr["start"] + text_block_annotation.start
            nr["end"] = nr["end"] + text_block_annotation.start
    return ner_results

ANNOTATION_TYPE_HF_NER = "hf_ner"
def get_text_blocks_annotations(document):
    tb_annotation_identifier = lambda a: a.extra_fields.get("dhs_type")=="text_block"
    return [a for a in document.annotations if tb_annotation_identifier(a)]
def document_text_blocks_entity_recognition(document, pipeline):
    """Does the Named entity recognition for the given Document, per annotated text_blocks
    /!\ Some text_blocks are too long. As of now, they are truncated /!\
    """

    tb_annotations = get_text_blocks_annotations(document)
    ner_results = [
        nr
        for tba in tb_annotations
        for nr in text_block_entity_recognition(document.text[tba.start:tba.end], pipeline, tba)
    ]
    ner_annotations = [
        Annotation(nr["start"], nr["end"], extra_fields={
            "type": ANNOTATION_TYPE_HF_NER,
            "hf_score": nr["score"],
            "hf_entity_group": nr["entity_group"],
            "hf_word": nr["word"]
        })
        for nr in ner_results
    ]
    # remove hf_ner annotations if already present to nut duplicate.
    document.annotations = [
        a for a in document.annotations
        if a.extra_fields.get("type")!=ANNOTATION_TYPE_HF_NER
    ]
    document.annotations += ner_annotations
    document.update_mentions()

    return ner_results

# %%

dhs_article = sampled_articles_dtf.article.iloc[78]
#dhsa_ner_results = article_entity_recognition(dhs_article, ner_pipeline)

# %%

# Investigation into text_blocks that are too long.
# dhs_article i=78 has a 630 tokens block!
if False:
    for i in range(32,79):
        print(i)
        dhs_article = sampled_articles_dtf.article.iloc[i]
        tokenized =[
                len(tokenizer(text, return_tensors="pt").input_ids[0])# , padding=True, truncation=True
                for tag, text in dhs_article.text_blocks
            ]
        #len(tokenized[0].input_ids)
        tokenized.sort()
    tokenized

    ## %%

    tokenized =[
            len(tokenizer(text, return_tensors="pt").input_ids[0])# , padding=True, truncation=True
            for i in range(0,100)
            for tag, text in sampled_articles_dtf.article.iloc[i].text_blocks
    ]
    #len(tokenized[0].input_ids)
    tokenized.sort()
    text_blocks_lg_512 = [t for t in tokenized if t>512]
    print(f"total nb paragraphs: {len(tokenized)}")
    print(f"nb paragraphs>512 tokens: {len(text_blocks_lg_512)}")
    print(f"proportion paragraphs>512 tokens: {np.round(len(text_blocks_lg_512) / len(tokenized),3)}")


# %%

# Investigation in how to use Document and their text_block annotations

i=78
dhs_article = sampled_articles_dtf.article.iloc[i]
spacy_doc = sampled_articles_dtf.spacy_doc.iloc[i]
doc = sampled_articles_dtf.document.iloc[i]

# %%

tb_annotations = [a for a in doc.annotations if a.extra_fields.get("dhs_type")=="text_block"]
tb_annotations
#for i, tba in enumerate(tb_annotations):

tbi = 1
tb_annotations[tbi]

#doc.reverse_consecutive_replace_span(doc.extra_fields["initial_replacement"])
#doc.text[tb_annotations[tbi].start:tb_annotations[tbi].end]  == dhs_article.text_blocks[tbi][1]
# -> yes!!

# %%

ner_results = document_text_blocks_entity_recognition(doc, ner_pipeline)
ner_results
# %%
sampled_articles_dtf.head()
# %%

def articles_dtf_entity_recognition(articles_dtf, ner_pipeline, force_recompute=False):
    """does the entity-recognition on the articles
    + adds the following columns:
        - ner_results: list of ner results from the hf pipeline (per hf-text-block of the max length accepted by the hf pipeline)
        + toponym_tokens_spans: list of spacy.Span of the recognized entities
    
    /!\ Some text_blocks are too long. As of now, they are truncated /!\
    """

    # easy way, problems:
    # - some text_blocks are longer than the allowed 512 tokens
    # - the initials aren't replaced in the text_blocks
    # solution: use sampled_articles_dtf.document and its text_blocks annotations
    # -> handles initials replacement already
    # -> can cut the text as needed
    # algo: 
    if "ner_results" not in articles_dtf or force_recompute:
        #articles_dtf["ner_results"] = articles_dtf.article.apply(lambda a: article_entity_recognition(a.text_blocks, ner_pipeline))
        ner_results = [
            #tb_annotations = [a for a in doc.annotations if a.extra_fields.get("dhs_type")=="text_block"]
            #text_blocks = [doc.text[a.start:a.end] for a in tb_annotations]
            document_text_blocks_entity_recognition(doc, ner_pipeline)
            for i, doc in tqdm(enumerate(articles_dtf.document), total = articles_dtf.shape[0], desc ="Computing NER...")
        ]
        articles_dtf["ner_results"] = ner_results

    articles_dtf["toponym_tokens_spans"]=[
        [
            row.spacy_doc.char_span(nr["start"], nr["end"], alignment_mode="expand")
            for nr in row.ner_results if nr["entity_group"]=="LOC"
        ]
        for i, row in articles_dtf.iterrows()
    ]

# %%

articles_dtf_entity_recognition(sampled_articles_dtf, ner_pipeline)

# %%
sampled_articles_dtf.head()

# %%

doc_index = 78
sampled_articles_dtf.toponym_tokens_spans.iloc[doc_index]
print(f"len spacy_doc: {len(sampled_articles_dtf.spacy_doc.iloc[doc_index].text)}")
print(f"len document: {len(sampled_articles_dtf.document.iloc[doc_index].text)}")
print(f"doc.text == spacy_doc.text: {sampled_articles_dtf.document.iloc[doc_index].text ==sampled_articles_dtf.spacy_doc.iloc[doc_index].text}")

# %%


sampled_articles_dtf.ner_results.iloc[doc_index]

# %%

sp_text = sampled_articles_dtf.spacy_doc.iloc[doc_index].text
doc_text = sampled_articles_dtf.document.iloc[doc_index].text
text_comparison = ""
diff_count = 0
diff_set = set()
for i, sp_char in enumerate(sp_text):
    if sp_char==doc_text[i]:
        text_comparison += sp_char
    else:
        text_comparison += f"-XXXXXXX ({sp_char})vs({doc_text[i]})-"
        diff_count+=1
        diff_set.add((sp_char, doc_text[i]))

print("diff_count:", diff_count)
print("diff_set:", diff_set)
text_comparison
# %%




def json_dump_huggingface_ner_results(dhs_article, dhsa_ner_results, jsonfile="huggingface_ner_results.json"):
    with open(jsonfile, "w") as nerf:
        json.dump({
            "hds_article_id": dhs_article.id,
            "text_blocks": dhs_article.text_blocks,
            "ner_results": dhsa_ner_results
        }, nerf, indent="\t", ensure_ascii=False)

def displacy_ner_results(text, ner_results, included_ents=["LOC", "DATE", "PER"]):
    tokens = []
    ents = []
    for i, nr in enumerate(ner_results):
        print("\tstart:", nr["start"], ", end:", nr["end"])
        if i!=0:
            prev_nr = ner_results[i-1]
            if nr["start"] > prev_nr["end"] :
                tokens.append(text[prev_nr["end"]:nr["start"]])
                ents.append("O")
        tokens.append(text[nr["start"]:nr["end"]])
        if nr["entity_group"] in included_ents:
            ents.append("B-"+nr["entity_group"])
        else:
            ents.append("O")
    ents = [e for i, e in enumerate(ents) if len(tokens[i])>0]
    return [t for t in tokens if len(t)>0], ents


def displacy_show_NER(text, ner_results, included_ents=["LOC", "DATE", "PER"]):
    tokens, ents = displacy_ner_results(text, ner_results, included_ents)
    print("\n\n\nTOKENS:\n")
    print(tokens)
    print("\n\n\n")
    doc = Doc(Vocab(strings=set(tokens)),
            words=tokens,
            # spaces=spaces,
            ents=ents
    )
    return displacy.render(doc, style="ent")



# %%


displacy_show_NER(sampled_articles_dtf.document.iloc[doc_index].text, sampled_articles_dtf.ner_results.iloc[doc_index])
# %%

displacy_show_NER(doc.text, ner_results)


# %%

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

tokens, ents =  displacy_article_ner_results(dhs_article.text_blocks, dhsa_ner_results)
displacy_dhs_article_NER(dhs_article, dhsa_ner_results)
# %%
# %%
json_dump_huggingface_ner_results(dhs_article, dhsa_ner_results, jsonfile="huggingface_ner_results.json")



# %%


# %%

i = 39
dhs_article = sampled_articles_dtf.article.iloc[i]
dhsa_ner_results = sampled_articles_dtf.ner_results.iloc[i]
print(dhs_article.id)
displacy_dhs_article_NER(dhs_article, dhsa_ner_results)

# %%
