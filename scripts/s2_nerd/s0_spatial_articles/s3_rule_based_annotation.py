
# %%
import unicodedata

import sys
sys.path.append("../../../src")
sys.path.append("../../../scripts")
from inception_fishing import Annotation
from s2_prepare_articles import *


import spacy

# %%
spacy_tokenizer = spacy.load("fr_core_news_sm")



# %%
# Evaluating normalized text difference with original text:

polities_dtf["normalized_text"] = polities_dtf.document.apply(lambda d: unicodedata.normalize("NFKC",d.text))

polities_dtf["len_normalized_text"] = polities_dtf["normalized_text"].apply(len)
polities_dtf["len_unnormalized_text"] = polities_dtf.document.apply(lambda d: len(d.text))
polities_dtf["len_diff_normalized_text"] = polities_dtf["len_unnormalized_text"] - polities_dtf["len_normalized_text"]
polities_dtf["len_diff_normalized_text"].value_counts()

# %%
# Character normalization investigation -> NFKC is the way to go :-)

# Zoug had a very big 2529 char diff using NFKD
lendif2529NFKD = polities_dtf[polities_dtf["hds_article_id"]=="007373"]

def investigate_norm_len_diff(dtf, i=0):
    norm_text = dtf["normalized_text"].iloc[i]
    unnorm_text = dtf.document.iloc[i].text

    norm_chars = set(norm_text)
    unnorm_chars = set(unnorm_text)

    unnorm_missing_chars = [ c for c in unnorm_chars if c not in norm_chars]
    norm_missing_chars = [ c for c in norm_chars if c not in unnorm_chars]

    #return (norm_text, unnorm_text, norm_chars, unnorm_chars, norm_missing_chars, unnorm_missing_chars)
    return (norm_missing_chars, unnorm_missing_chars)

investigate_norm_len_diff(lendif2529NFKD)

# %%

lendifNFKC = polities_dtf[polities_dtf["len_diff_normalized_text"]!=0]

"""Still some problem with some minor characters... we'll come to it when we need ta
Funny enough... when running this script as ipynb: no problem... Still these are the 3 problematic one if further inspection is needed"""
polities_dtf.loc[polities_dtf.polity_id.apply(lambda i: i in ["001256-c", "001321-c", "007384-ct"]),:]


[investigate_norm_len_diff(lendifNFKC, i) for i in range(lendifNFKC.shape[0])]


# %%

def normalize_unicode_text(text):
    """unicode normalization NFKD removes accents in characters -> NFKC is the way to go :-)
    
        /!\\ /!\\ /!\\ normalizing text yields different text lengths for 3 articles (out of 4000), use with caution /!\\/!\\/!\\
        but it is needed for proper tokenization/prediction/learning"""

    return unicodedata.normalize("NFKC",text)

#%%
grandson_dtf = polities_dtf[polities_dtf.toponym=="Grandson"]
grandson_article = grandson_dtf.article.iloc[0]
grandson_document = grandson_dtf.document.iloc[0]
doc = spacy_tokenizer(normalize_unicode_text(grandson_document.text))

# %%

grandson_tokens = [token for token in doc if token.text =="Grandson"]

grandson_tokens
# %%
seigneurs_tokens = [token for token in doc if token.text =="seigneurs"]
[seigneurs_tokens[0].nbor(i) for i in range(-5,5)]
# %%
nb_prev = 2

grandson_tokens_3g = [[t.nbor(i) for i in range(-nb_prev,1)] for t in grandson_tokens]

grandson_tokens_3g

# %%

"""
Strategy rule-based annotations:
- tokenize list of articles
    - use doc text
    - normalize
- frequency table of N predecessor words
    -> identify the ones that are relevant statuswords
- extract all sequences of the form statuswords-X-X-toponym
- identify the relevant sequences representing an entity
- identify which entity each sequence corresponds to
    -> each statuswords refers to a list of possible entity type
    -> entity type + statusword

"""

# %%

def normalize_doc_text(d):
    """ /!\\ use with caution, see above"""
    d.text = normalize_unicode_text(d.text)

polities_dtf.document.apply(normalize_doc_text)
""

# %%
sampled_articles_ids = set(sampled_articles_ids)
#sampled_polities_dtf = polities_dtf[polities_dtf.hds_article_id.apply(lambda id: id in sampled_articles_ids)]

# %%

additional_columns = ["article", "document"]
articles_dtf = get_articles_dtf_from_polities_dtf(polities_dtf, additional_columns)

# %%


# %%

# take into account the fact that toponym might span multiple tokens
articles_dtf["tokenized_toponym"] = articles_dtf.toponym.apply(lambda t: set([tok.text for tok in spacy_tokenizer(normalize_unicode_text(t))]))
toponym_tokens = articles_dtf["tokenized_toponym"].explode()
#[t for t in utoponym_tokens if len(t)==4]
toponym_tokens_value_counts = toponym_tokens.value_counts()
toponym_tokens_value_counts[toponym_tokens_value_counts>1].shape
toponym_tokens_value_counts.shape


#with pd.option_context('display.max_rows', None, 'display.max_columns', None):
toponym_tokens_value_counts

# %%
not_toponym_tokens = {"'",
 '-',
 '/',
 "L'",
 'La',
 'Lac',
 'Le',
 'Les',
 'Nord',
 'S',
 'See',
 'Sud',
 'Sur',
 'am',
 'an',
 'bei',
 'ch',
 "d'",
 'da',
 'dans',
 'de',
 'der',
 'des',
 'di',
 'du',
 'et',
 'im',
 'in',
 'l',
 'la',
 'le',
 'les',
 'près',
 'sur',
 'zum',
 "vers"
}
ambiguous_toponym_tokens={
 'Au',
 'Bois',
 'Col',
 'Dieu',
 'Eaux',
 'Ile',
 'Part',
 'Pays',
 'Pont',
 'Port',
 'Rue',
 "vaudois",
 "helvétique",
}

# %%

articles_dtf["loose_normalized_tokenized_toponym"] = [[s for s in texts if s not in not_toponym_tokens] for texts in articles_dtf["tokenized_toponym"]]
articles_dtf["strict_normalized_tokenized_toponym"] = [[s for s in texts if s not in ambiguous_toponym_tokens] for texts in articles_dtf["loose_normalized_tokenized_toponym"]]

# %%

normalized_toponym_tokens = set(articles_dtf["strict_normalized_tokenized_toponym"].explode())


# %%

sampled_articles_dtf = articles_dtf[articles_dtf.hds_article_id.apply(lambda id: id in sampled_articles_ids)].copy()

sampled_articles_dtf["tokens"] = sampled_articles_dtf.document.apply(lambda d: spacy_tokenizer(normalize_unicode_text(d.text)))

# %%

def is_token_toponym(token, dtf_row):
    """Checks that a given token isn't a toponym (either corresponding to any strict toponym, or a loose toponym from the particular article toponym"""
    return (
        token.text in normalized_toponym_tokens
        or token.text in dtf_row.loose_normalized_tokenized_toponym
    )
# %%

# toponym_tokens: tokens in the text that denote a toponym
sampled_articles_dtf["toponym_tokens"] = [
    # handle the case of multiple toponym tokens: in this case only take first token each time
    [
        token for token in row.tokens
        if is_token_toponym(token, row)
        and (token.i==0 or not is_token_toponym(token.nbor(-1), row))
    ]
    for k, row in sampled_articles_dtf.iterrows()
]

# %%

nb_predecessors = 10
nb_successors = 3
sampled_articles_dtf["predecessors_tokens"] = [[
        #(print(f"nb_successors={nb_successors}, len(t.doc)={len(t.doc)}, t.i={t.i}, len(t.doc)-t.i)+1={(len(t.doc)-t.i)+1}, total={min(nb_successors, len(t.doc)-t.i)}"),
        t.nbor(i)
        for t in row.toponym_tokens for i in range(-min(nb_predecessors,t.i),min(nb_successors, len(t.doc)-t.i))
    ]
    for k, row in sampled_articles_dtf.iterrows()
]
predecessors_tokens = sampled_articles_dtf["predecessors_tokens"].apply(lambda ts: [t.text for t in ts]).explode()
predecessors_tokens_value_counts = predecessors_tokens.value_counts().to_frame()
predecessors_tokens_value_counts.to_csv("predecessors_tokens_value_counts.csv", sep="\t")

# %%

#pd.set_option('display.max_rows', None)
predecessors_tokens_value_counts[predecessors_tokens_value_counts.predecessors_tokens==2]

statusword_token_text = [
    # lordships
    "seigneur",
    "seigneurs",
    "seigneurie",
    "seigneuries",
    "châtellenie",
    "châtellenies",
    "comte",
    "comtes",
    "comté",
    "comtés",
    "baron",
    "barons",
    "baronnie",
    "baronnies",
    "duc",
    "ducs",
    "duché",
    "duchés",
    # cantons
    "canton",
    "cantons",
    # administrative: district/bailliage/etc
    "district",
    "districts",
    "distr",
    "dizain",
    "dizains"
    "bailliage",
    "bailliages",
    "bailli",
    "baillis",
    # commmunes
    "commune",
    "communes",
    "comm",
    "village",
    "villages",
    "municipalité",
    "municipalités"
    "communauté",
    "communautés",
    "munizipalgemeinde",
    "ortsgemeinden",
    "ville",
    "hameau",
    "hameaux",
    "paroisse",
    "paroisses",
    "bourgade",
    "bourgades",
    "localité",
    "localités",
    "cercle",
    "cercles",
    # ecclesiastical
    "chapitre",
    "prieuré",
    "prieurés",
    "abbaye",
    "abbayes",
    "abbé",
    "abbés",
    "évêque",
    "évêques",
    "évêché",
    "évêchés",
    "diocèse",
    "diocèses",
    "monastère",
    "monastères",
    "avouerie",
    "avoueries",
    "commanderie",
    "commanderies",
    # fuzzy terms
    "région",
    "régions",
    "domaine",
    "domaines",
    "vallon",
    "administration",
    "circonscriptions",

]

ambiguous_statusword_token_text = [
    "vallée",
    "château",
    "châteaux"
    "terres",
    "territoire",
    "église",
    #"dîme", # -> ?
    "juridictions",
    "juridiction",
    "forêt",
    "forêts",
    "possession",
    "possessions",
    "ferme",
    "fermes",
    "suzeraineté",
    #"vestiges",# -> ?
    #"hôpital",

]
# %%

sampled_articles_dtf["toponyms_tokens_sequences"] = [
    [
        [t.nbor(i) for i in range(-min(nb_predecessors,t.i),min(nb_successors, len(t.doc)-t.i))]
        for t in row.toponym_tokens
    ]
    for k, row in sampled_articles_dtf.iterrows()
]
# %%
toponyms_tokens_sequences = [
    seq for toponyms_tokens_sequences in sampled_articles_dtf.toponyms_tokens_sequences
    for seq in toponyms_tokens_sequences
]
# %%

sampled_articles_dtf["statusword_tokens_sequences"] = [
    [seq for seq in toponyms_tokens_sequences if any(token.text.lower() in statusword_token_text for token in seq)]
    for toponyms_tokens_sequences in sampled_articles_dtf.toponyms_tokens_sequences
]
# %%

statusword_tokens_sequences = [
    seq for statusword_tokens_sequences in sampled_articles_dtf.statusword_tokens_sequences
    for seq in statusword_tokens_sequences
]

# %%

def analyse_statusword_tokens_sequence_single(dtf_row, token_sequence, statusword_index, toponym_index):
    """Analyses a single statusword-toponym combination

    returns a sequence whose first term is the sequence's statusword, and the last word is the sequence's toponym
    """
    sequence = token_sequence[statusword_index:(toponym_index+1)]
    sequence_structure = [
        "STATUS" if token.text.lower() in statusword_token_text else(
        "TOPONYM" if is_token_toponym(token, dtf_row)
        else token.text
        )
        for token in sequence
    ]
    statusword = token_sequence[statusword_index]
    toponym = token_sequence[toponym_index]
    return (statusword, toponym, sequence, sequence_structure)

def analyse_statusword_tokens_sequence(dtf_row, token_sequence):
    """Returns all the possible statusword-toponym combination analyses for a given token sequence
    """
    statusword_indices = [i for i,tok in enumerate(token_sequence) if tok.text.lower() in statusword_token_text]
    #toponym_indices = [i for i,tok in enumerate(token_sequence) if tok.text in normalized_toponym_tokens or tok.text in dtf_row.loose_normalized_tokenized_toponym]
    toponym_indices = [len(token_sequence)-nb_successors] # the toponym is always at the same spot in the sequence
    sequences_analyses = [
        analyse_statusword_tokens_sequence_single(dtf_row, token_sequence, i, j)
        for i in statusword_indices for j in toponym_indices if i<j
    ]
    return sequences_analyses

# %%
statusword_tokens_sequences_dtf = sampled_articles_dtf.explode("statusword_tokens_sequences")
statusword_tokens_sequences_dtf = statusword_tokens_sequences_dtf[['hds_article_id', 'toponym', 'geoidentifier', 'article_title', 'polities_ids', 'nb_polities',
       'tokenized_toponym', 'loose_normalized_tokenized_toponym',
       'strict_normalized_tokenized_toponym',
       'statusword_tokens_sequences']].copy()

statusword_tokens_sequences_dtf = statusword_tokens_sequences_dtf[~statusword_tokens_sequences_dtf.statusword_tokens_sequences.isna()]

# %%
statusword_tokens_sequences_dtf["sequence_analysis"] = [
    analyse_statusword_tokens_sequence(row, row.statusword_tokens_sequences)
    for k, row in statusword_tokens_sequences_dtf.iterrows()
]

# %%

sequences_analyses_dtf = statusword_tokens_sequences_dtf.explode("sequence_analysis")
sequences_analyses_dtf = sequences_analyses_dtf[~sequences_analyses_dtf.sequence_analysis.isna()]
sequences_analyses_dtf["statusword"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[0])
sequences_analyses_dtf["sequence_toponym"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[1])
sequences_analyses_dtf["sequence"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[2])
sequences_analyses_dtf["sequence_structure"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[3])
sequences_analyses_dtf["sequence_structure_str"] = sequences_analyses_dtf["sequence_structure"].apply(lambda ss: "-".join(ss))
sequence_structures = sequences_analyses_dtf["sequence_structure_str"].value_counts()

# %%

sequence_structures
sequence_structures.to_frame().to_csv(s2_sequence_structures_counts_csv, sep="\t")
sequence_structures[sequence_structures>3]

# %%

sequence_structure = "STATUS-\n-Dizain-du-TOPONYM"

sequence_structures_human_columns = ['toponym', 'article_title', 'polities_ids', "statusword", "sequence", "sequence_structure"]

sequences_analyses_dtf.loc[sequences_analyses_dtf["sequence_structure_str"]==sequence_structure,sequence_structures_human_columns]
# %%

valid_sequence_structures = pd.read_csv(s2_sequence_structures_validation_csv, sep="\t")
valid_sequence_structures = set(valid_sequence_structures[valid_sequence_structures.validity=="yes"].structure)
valid_sequence_structures

# %%

sequence_structures.shape
# %%

valid_sequences_dtf = sequences_analyses_dtf[sequences_analyses_dtf.sequence_structure_str.apply(lambda struct: struct in valid_sequence_structures)].copy()
valid_sequences_dtf.shape

# %%



with open(s2_statusword_to_typology_json) as f:
    statusword_keys_dict = json.load(f)

statusword_to_typology_dict = {
    statusword : t[1] 
    for t in statusword_keys_dict
    for statusword in t[0]
}

statusword_to_hdstag_dict = {
    statusword : t[2] 
    for t in statusword_keys_dict
    for statusword in t[0]
}

# %%

polities_dtf[polities_dtf.typology=="baillage"].tail()

# %%


polities_dtf["tokenized_toponym"] = polities_dtf.toponym.apply(lambda t: spacy_tokenizer(t))
polities_dtf["tokenized_toponym_texts"] = polities_dtf.tokenized_toponym.apply(lambda tokens: [t.text for t in tokens])

polities_dtf["tokenized_toponym"].apply(len).value_counts()
polities_dtf[polities_dtf["tokenized_toponym"].apply(len)>1]

# %%

# %%

def link_entity_by_typology(dtf_row, polities_dtf):
    possible_typologies = statusword_to_typology_dict.get(dtf_row.statusword.text.lower())

    if possible_typologies is None:
        print("WARNING: statusword without corresponding typology: |"+dtf_row.statusword.text.lower()+"|")
        return []

    possible_polities = [
        polities_dtf.loc[(polities_dtf.typology==typology) & polities_dtf.toponym.apply(lambda t: dtf_row.sequence_toponym.text == t)]
        for typology in possible_typologies
    ]
    possible_polities = [dtf for dtf in possible_polities if dtf.shape[0]>0]
    return possible_polities

def count_nb_matching_tokens(sequence_dtf_row, tokenized_toponym_texts):
    sequence_dtf_row_tokens_texts = [t.text for t in sequence_dtf_row.statusword_tokens_sequences]
    nb_matching_tokens = sum([
        word in sequence_dtf_row_tokens_texts[-(nb_successors+1):]
        for word in tokenized_toponym_texts
    ])
    return nb_matching_tokens

def link_entity_by_hdstag(dtf_row, polities_dtf, statusword_to_hdstag_dict):
    """
        # find possible polities: take polities that have matching hds_tag AND an exact match between the searched toponym and th sequence's identified toponym

    replacement proposition:
    - tokenize polities_dtf canonic_title
    - computing toponym matching score

    toponym matching score:
    - nb_matching_tokens= nb of polities_dtf.toponym_tokens present in sequence_tokens
    - all_tokens_matched: whether all tokens of the polities_dtf.toponym_tokens are in the sequence_tokens 
    - hds_tag_score: score inversely proportional to the rank an hds_tag has in the ordering (rank 0 -> highest score)

    ranking algorithm:
    -> order according to following order:
        1) all_tokens_matched*nb_matching_tokens
        2) hds_tag_score
        3) nb_matched_tokens
    -> score = 100* all_tokens_matched*nb_matching_tokens +
                10 * hds_tag_score + 
                nb_matched_tokens
    """
    possible_hdstags = statusword_to_hdstag_dict.get(dtf_row.statusword.text.lower())

    if possible_hdstags is None:
        print("WARNING: statusword without corresponding hdstag: |"+dtf_row.statusword.text.lower()+"|")
        return []

    possible_polities = [(
            i,
            polities_dtf.loc[(polities_dtf.hds_tag==hds_tag) &
            polities_dtf.tokenized_toponym_texts.apply(lambda tokens:
                any([dtf_row.sequence_toponym.text == t for t in tokens])
            )].copy()
        )for i,hds_tag in enumerate(possible_hdstags)
    ]
    for i,dtf in possible_polities:
        dtf["possibility_hds_tag_rank"] = i 
    possible_polities_dtf = pd.concat([dtf for i,dtf in possible_polities])
    possible_polities_dtf["nb_matching_tokens"] = possible_polities_dtf.tokenized_toponym_texts.apply(lambda ttt: count_nb_matching_tokens(dtf_row, ttt))
    possible_polities_dtf["possible_polity_score"] = \
        100* (possible_polities_dtf.tokenized_toponym_texts.apply(len)==possible_polities_dtf["nb_matching_tokens"]) * possible_polities_dtf["nb_matching_tokens"] + \
        10* (possible_polities_dtf["possibility_hds_tag_rank"].max() - possible_polities_dtf["possibility_hds_tag_rank"])+ \
        possible_polities_dtf["nb_matching_tokens"]
    possible_polities_dtf = possible_polities_dtf.sort_values(by ='possible_polity_score', ascending = False)

    return possible_polities_dtf

# %%

valid_sequences_dtf["possible_polities"] = [
    link_entity_by_hdstag(row, polities_dtf, statusword_to_hdstag_dict)
    for i, row in valid_sequences_dtf.iterrows()
]

#valid_sequences_dtf["possible_polities_ranks"] = valid_sequences_dtf["possible_polities"].apply(lambda pp: [t[0] for t in pp])
valid_sequences_dtf["possible_polities_min_rank"] = valid_sequences_dtf["possible_polities"].apply(lambda pp_dtf: pp_dtf.possibility_hds_tag_rank.min() if pp_dtf.shape[0]>0 else None)
# %%
if False:
    valid_sequences_dtf["possible_polities_by_typology"] = [
        link_entity_by_typology(row, polities_dtf)
        for i, row in valid_sequences_dtf.iterrows()
    ]

# %%

valid_sequences_dtf["possible_polities"].apply(lambda pp_dtf: pp_dtf.shape[0]).value_counts()
valid_sequences_dtf["possible_polities_min_rank"].value_counts()

# %%

valid_sequences_dtf["linked_polity_id"] = valid_sequences_dtf["possible_polities"].apply(lambda pp: pp.iloc[0]["polity_id"] if pp.shape[0]>0 else None)
valid_sequences_dtf["linked_hds_tag"] = valid_sequences_dtf["possible_polities"].apply(lambda pp: pp.iloc[0]["hds_tag"]if pp.shape[0]>0 else None)
valid_sequences_dtf["linked_toponym"] = valid_sequences_dtf["possible_polities"].apply(lambda pp: pp.iloc[0]["toponym"]if pp.shape[0]>0 else None)

# %%

linked_sequences_human_columns = ["hds_article_id", "statusword", "sequence_toponym", "sequence", "linked_polity_id", "linked_hds_tag", "linked_toponym"]

valid_sequences_dtf.loc[:,linked_sequences_human_columns]

# %%

linked_sequences_dtf = valid_sequences_dtf.loc[valid_sequences_dtf["possible_polities"].apply(lambda pp: pp is not None)].copy()
linked_sequences_dtf.loc[:,linked_sequences_human_columns]


# %%

unlinked_sequences_human_columns = ["hds_article_id", "statusword", "sequence_toponym", "sequence"]

unlinked_sequences_dtf = valid_sequences_dtf.loc[valid_sequences_dtf["possible_polities"].apply(lambda pp: pp is None)].copy()
unlinked_sequences_dtf.loc[:,unlinked_sequences_human_columns]

# %%

polities_dtf[polities_dtf.typology.apply(lambda t: t is None)].hds_tag.value_counts()


# %%

def add_annotation_to_document_from_valid_sequences(document, valid_sequences_dtf_rows):
    new_annotations = [
        Annotation(
            row.sequence[0].idx,
            row.sequence[-1].idx+len(row.sequence[-1]),
            extra_fields={
                "type": "polity_id_LOC",
                "polity_id": row.linked_polity_id
            }
        )
        for i, row in valid_sequences_dtf_rows.iterrows()
    ]
    document.annotations = document.annotations + new_annotations

# %%

for i, row in sampled_articles_dtf.iterrows():
    add_annotation_to_document_from_valid_sequences(row.document, valid_sequences_dtf[valid_sequences_dtf.hds_article_id==row.hds_article_id])
# %%



#%%

# COMPLETING ANNOTATIONS OF MULTI-TOKEN TOPONYMS
sampled_articles_dtf.iloc[32,:].hds_article_id

valid_sequences_dtf[valid_sequences_dtf.hds_article_id=="001245"]
dtf_row = valid_sequences_dtf[valid_sequences_dtf.hds_article_id=="001245"].iloc[1,:]

valid_sequences_dtf[valid_sequences_dtf.hds_article_id=="001245"].iloc[0,:].possible_polities

#hds_tag = valid_sequences_dtf.loc[valid_sequences_dtf.hds_article_id=="001245",["hds_tag"]]

# %%
