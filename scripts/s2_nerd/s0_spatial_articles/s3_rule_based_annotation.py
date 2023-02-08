#!/usr/bin/env python
# coding: utf-8

# %%


import unicodedata

import sys
import re
from os import path

sys.path.append("../../../src")
sys.path.append("../../../scripts")
from inception_fishing import Annotation

from tqdm import tqdm


from importlib import reload


# %%


from s2_prepare_articles import *
import spacy


# %%



from spatial_articles_utils import *

# if updating spatial_articles_utils, run this code:
#get_ipython().run_line_magic('run', '-m spatial_articles_utils')


# %%





# %%


spacy_tokenizer = spacy.load("fr_core_news_sm")


# # Documents' text preparation
# ## Normalizing texts and investigating text issues

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

"""Still some problem with some minor characters... we'll come to it when we need ta"""
polities_dtf.loc[polities_dtf.polity_id.apply(lambda i: i in ["001256-c", "001321-c", "007384-ct"]),:]


[investigate_norm_len_diff(lendifNFKC, i) for i in range(lendifNFKC.shape[0])]


# %%


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


polities_dtf.drop(
    ["normalized_text", "len_normalized_text", "len_unnormalized_text",
    "len_diff_normalized_text", "len_diff_normalized_text"],
    axis=1,
    inplace=True
)
if False:

    def normalize_doc_text(d):
        """ /!\\ use with caution, see above"""
        d.text = normalize_unicode_text(d.text)

    polities_dtf.document.apply(normalize_doc_text)
    ""


# %%


sampled_articles_ids = set(sampled_articles_ids)
#sampled_polities_dtf = polities_dtf[polities_dtf.hds_article_id.apply(lambda id: id in sampled_articles_ids)]


# %%


polities_dtf.geoidentifier.unique()


# #  Polity recognition
# 
# ## Identifying toponyms' tokens

# %%


# take into account the fact that toponym might span multiple tokens
#articles_dtf["tokenized_toponym"] = articles_dtf.toponym.apply(lambda t: set([tok.text for tok in spacy_tokenizer(normalize_unicode_text(t))]))
add_toponyms(polities_dtf, spacy_tokenizer)
toponym_tokens = polities_dtf["tokenized_toponym"].explode().apply(lambda t: t.text)
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


#articles_dtf["loose_normalized_tokenized_toponym"] = [[s for s in texts if s not in not_toponym_tokens] for texts in articles_dtf["tokenized_toponym"]]
#articles_dtf["strict_normalized_tokenized_toponym"] = [[s for s in texts if s not in ambiguous_toponym_tokens] for texts in articles_dtf["loose_normalized_tokenized_toponym"]]

#normalized_toponym_tokens = set(articles_dtf["strict_normalized_tokenized_toponym"].explode())

normalized_toponym_tokens, trimmed_normalized_tokenized_toponyms_texts = normalize_toponyms(polities_dtf, not_toponym_tokens, ambiguous_toponym_tokens)

polities_dtf.tokenized_toponym


# %%


additional_columns = [
    "article", "document", "tokenized_toponym",
    "trimmed_normalized_tokenized_toponym", "loose_normalized_tokenized_toponym", "strict_normalized_tokenized_toponym"]
articles_dtf = get_articles_dtf_from_polities_dtf(polities_dtf, additional_columns)
polities_dtf["tokenized_toponym_texts"] = [[t.text for t in tokens] for tokens in polities_dtf.tokenized_toponym]


# %%


sampled_articles_dtf = articles_dtf[articles_dtf.hds_article_id.apply(lambda id: id in sampled_articles_ids)].copy()

#sampled_articles_dtf["spacy_doc"] = sampled_articles_dtf.document.apply(lambda d: spacy_tokenizer(normalize_unicode_text(d.text)))
add_tokenized_text(sampled_articles_dtf, spacy_tokenizer)
sampled_articles_dtf.head()


# %%


# toponyms_pattern regex test
if False:
    trimmed_normalized_tokenized_toponyms_texts

    toponyms_pattern = re.compile("("+(r")\W|\W(".join(trimmed_normalized_tokenized_toponyms_texts))+")")
    text = " "+sampled_articles_dtf.document.iloc[0].text+" "

    match_list = [m for m in toponyms_pattern.finditer(text)] #, re.IGNORECASE)]
    (text, match_list)


# %%


# might simple string operation be faster than regex? who knows...
def find_indices(string, substring):
    """returns all the start+end boundaries of the occurences of the substring inside the string"""
    indices = [(index,len(substring)) for index in range(len(string)) if string.startswith(substring, index)]
    return indices

a_string = "the quick brown fox jumps over the lazy dog. the quick brown fox jumps over the lazy dog"
# Find all indices of 'the'
indices = [index for index in range(len(a_string)) if a_string.startswith('the', index)]
print(indices)


# %%





# %%


#add_text_toponyms_spans(sampled_articles_dtf, trimmed_normalized_tokenized_toponyms_texts)

sampled_articles_dtf = restore_or_compute_and_save_toponym_spans(sampled_articles_dtf, s2_toponyms_spans_dtf_pickle, trimmed_normalized_tokenized_toponyms_texts)
sampled_articles_dtf.head()


# %%




toponyms_dtf = to_toponyms_dtf(sampled_articles_dtf)
toponyms_dtf.head()


# ## Extracting toponym sequences

# %%


nb_predecessors = 10
nb_successors = 3
add_toponym_tokens_sequence(toponyms_dtf, nb_predecessors, nb_successors)


# %%


# toponym_sequence_tokens: all tokens present in any toponym sequence
toponym_sequence_tokens = toponyms_dtf.toponym_tokens_sequence.apply(lambda span:
    [t.text for t in span]
).explode()

toponym_sequence_tokens_value_counts = toponym_sequence_tokens.value_counts().to_frame()
toponym_sequence_tokens_value_counts.columns = ['toponym_sequence_tokens']
toponym_sequence_tokens_value_counts.to_csv("toponym_sequence_tokens_value_counts.csv", sep="\t")


# %%


toponym_sequence_tokens_value_counts


# ### Differentiating single-toponym and statuswords-toponym sequences

# %%


#pd.set_option('display.max_rows', None)
toponym_sequence_tokens_value_counts[toponym_sequence_tokens_value_counts.toponym_sequence_tokens==2]
s2_statuswords_json = path.join(s2_polities_to_extract_folder, "statuswords.json")

with open(s2_statuswords_json) as f:
    statuswords_text = json.load(f)


ambiguous_statuswords_text = statuswords_text["ambiguous_statuswords"]
statuswords_text = statuswords_text["statuswords"]
statuswords_text


# %%


identify_statusword_toponym_sequences(toponyms_dtf, statuswords_text)
statusword_tokens_sequences_columns_filter =['hds_article_id', 'toponym', 'geoidentifier', 'article_title', 'polities_ids', 'nb_polities',
        'tokenized_toponym', "trimmed_normalized_tokenized_toponym", 'loose_normalized_tokenized_toponym',
        'strict_normalized_tokenized_toponym', "toponym_tokens_spans", 'toponym_tokens_sequence'
    ]
statusword_tokens_sequences_dtf = toponyms_dtf.loc[toponyms_dtf.is_statusword_toponym_sequence,statusword_tokens_sequences_columns_filter].copy()
only_toponyms_sequences_dtf = toponyms_dtf.loc[~toponyms_dtf.is_statusword_toponym_sequence,statusword_tokens_sequences_columns_filter].copy()

print("total nb of identified toponyms:", toponyms_dtf.shape[0])
print("nb of identified statusword+toponyms:", statusword_tokens_sequences_dtf.shape[0])
print("nb of single toponyms:",only_toponyms_sequences_dtf.shape[0])
print("check: nb of single+sw toponyms:", statusword_tokens_sequences_dtf.shape[0]+only_toponyms_sequences_dtf.shape[0])
print(toponyms_dtf.toponym_tokens_sequence.iloc[0])
print(statusword_tokens_sequences_dtf.toponym_tokens_sequence.iloc[0][0].i)
print(only_toponyms_sequences_dtf.toponym_tokens_sequence.iloc[0][0].i)
toponyms_dtf.head()


# ## Statusword-toponym combination
# 
# ### Analysing sequences structure
# STATUS-XX-TOPONYM

# %%





# %%





# %%


sequences_analyses_dtf, non_analysable_sequences_dtf = analyse_statuswords_toponyms_sequences(statusword_tokens_sequences_dtf, statuswords_text, normalized_toponym_tokens)
sequence_structures = sequences_analyses_dtf["sequence_structure_str"].value_counts()


# %%


sequence_structures
sequence_structures.to_frame().to_csv(s2_sequence_structures_counts_csv, sep="\t")
sequence_structures[sequence_structures>3]


# %%


sequence_structure = "STATUS-\n-Dizain-du-TOPONYM"

sequence_structures_human_columns = ['toponym', 'article_title', 'polities_ids', "statusword", "sequence", "sequence_structure"]

sequences_analyses_dtf.loc[sequences_analyses_dtf["sequence_structure_str"]==sequence_structure,sequence_structures_human_columns]


# ### Isolating valid statusword-toponym sequences structures

# %%


valid_sequence_structures = pd.read_csv(s2_sequence_structures_validation_csv, sep="\t")
valid_sequence_structures = set(valid_sequence_structures[valid_sequence_structures.validity=="yes"].structure)
valid_sequence_structures


# %%


sequence_structures.shape


# %%





# %%


valid_sequences_dtf, invalid_sequences_dtf = validate_statuswords_toponyms_sequences(sequences_analyses_dtf, valid_sequence_structures)
valid_sequences_dtf.shape


# ### Reintegration of invalid statusword-toponym sequences as single-toponyms
# 
# Reintegrates both invalid_sequences_dtf and non_analysable_sequences_dtf
# 
# algo:
# - remove all rows from invalid_sequences_dtf if toponym_tokens_spans is inside:
#     + valid_sequences_dtf.toponym_tokens_spans
#     + single_toponyms_sequences_dtf.toponym_tokens_spans
#     -> create set of tokens
# - remove duplicate invalid_sequences_dtf.toponym_tokens_spans
# - reunite it with only_toponyms_sequences_dtf
# 

# %%




# checking how spacy token/span equality&hashing works
# -> as we would like it to!
if False:
    doc1 = spacy_tokenizer("j'aime la crème glacée")
    doc2 = spacy_tokenizer("la crème suisse est vraiment glacée")
    doc1set = set([t for t in doc1])
    doc2set = set([t for t in doc2])
    print("doc1:", doc1)
    for i,t in enumerate(doc1):
        print(i,t)
    print("doc2:", doc2)
    for i,t in enumerate(doc2):
        print(i,t)
    print("membership test:")
    for i,t in enumerate(doc2):
        print(i,t)
        print("\t\tt in doc1", t in doc1, "\tt in doc1set", t in doc1set)
        print("\t\tt in doc2", t in doc2, "\tt in doc2set", t in doc2set)
        print("\t\t", "[t1==t for t1 in doc1]")
        print("\t\t", [t1==t for t1 in doc1])
        print("\t\t", "[t1==t for t1 in doc2]")
        print("\t\t", [t1==t for t1 in doc2])

    print("\nSpan tests:")
    span1 = doc1[2:4]
    span2 = doc1[2:4]
    span3 = doc2[2:4]
    span4 = doc2[0:2]
    print("spans: 1", span1, "2: ", span2, "3: ", span3, "4: ", span4)
    print("1==1:", span1==span1, "1==2:", span1==span2, "1==3:", span1==span3, "1==4:", span1==span4)



# %%


print(list(non_analysable_sequences_dtf.shape))
print(list(invalid_sequences_dtf.shape))


# %%


valid_sequence_toponyms = set([ t for t in valid_sequences_dtf.sequence_toponym])
sum([t in valid_sequence_toponyms for t in invalid_sequences_dtf.sequence_toponym])


# %%


invalid_sequences_dtf.toponym_tokens_spans.duplicated().sum()


# %%





# %%


print("reintegrating invalid_sequences_dtf:\n-----")
single_toponyms_sequences_dtf = reintegrate_dtf(invalid_sequences_dtf, only_toponyms_sequences_dtf, [valid_sequences_dtf])


# %%


print("reintegrating non_analysable_sequences_dtf:\n-----")
single_toponyms_sequences_dtf = reintegrate_dtf(non_analysable_sequences_dtf, single_toponyms_sequences_dtf, [valid_sequences_dtf])


# ## Getting polities_dtf toponyms' tokens

# %%


polities_dtf[polities_dtf.typology=="baillage"].tail()


# %%


#polities_dtf["tokenized_toponym"] = [spacy_tokenizer(t) for t in tqdm(polities_dtf.toponym, total=polities_dtf.shape[0], desc="Tokenizing polities' toponyms")]

polities_dtf["tokenized_toponym"].apply(len).value_counts()
polities_dtf[polities_dtf["tokenized_toponym"].apply(len)>1]


# # Polity linking

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


# 
# ## Linking single toponyms to their polity 

# %%


default_hdstag_priorization = statusword_keys_dict[0][2]
default_hdstag_priorization


# %%


toponyms_exact_match_dict = create_toponyms_exact_match_dict(polities_dtf, default_hdstag_priorization)
toponyms_exact_match_dict


# %%


#single_toponyms_sequences_dtf.toponym_tokens_spans[single_toponyms_sequences_dtf.toponym_tokens_spans.apply(len)>1].head()#iloc[1].text
link_single_toponyms(single_toponyms_sequences_dtf, polities_dtf, toponyms_exact_match_dict)


# %%


single_toponyms_sequences_dtf.head()


# %%


single_toponyms_sequences_dtf.possible_polities.apply(len).value_counts()


# %%


single_toponyms_sequences_dtf[single_toponyms_sequences_dtf.possible_polities.apply(len)>4].head()


# 
# ## Linking valid statuswords sequences to their polity 

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


# %%


link_statuswords_toponyms_sequences(valid_sequences_dtf, polities_dtf, statusword_to_hdstag_dict)


# %%


valid_sequences_dtf.possible_polities.iloc[0]


# %%


if False:
    valid_sequences_dtf["possible_polities_by_typology"] = [
        link_entity_by_typology(row, polities_dtf)
        for i, row in valid_sequences_dtf.iterrows()
    ]


# %%


valid_sequences_dtf["possible_polities"].apply(lambda pp_dtf: pp_dtf.shape[0]).value_counts()
valid_sequences_dtf["possible_polities_min_rank"].value_counts()


# ## Exploring linking results
# 
# ### Statusword-toponym linking results

# %%


linked_sequences_human_columns = ["hds_article_id", "statusword", "sequence_toponym", "sequence", "linked_polity_id", "linked_hds_tag", "linked_toponym"]

valid_sequences_dtf.loc[:,linked_sequences_human_columns]


# %%


linked_sequences_dtf = valid_sequences_dtf.loc[valid_sequences_dtf["possible_polities"].apply(lambda pp: pp.shape[0]>0)].copy()
linked_sequences_dtf.loc[:,linked_sequences_human_columns]


# %%


unlinked_sequences_human_columns = ["hds_article_id", "statusword", "sequence_toponym", "sequence"]

unlinked_sequences_dtf = valid_sequences_dtf.loc[valid_sequences_dtf.linked_polity_id.apply(lambda lpi: lpi is None)].copy()

print("Number of unlinked statusword-toponym sequences:", unlinked_sequences_dtf.shape[0])
unlinked_sequences_dtf.loc[:,unlinked_sequences_human_columns]


# %%


unlinked_sequences_dtf["sequence_text"] = ["".join([t.text_with_ws for t in s]) for s in unlinked_sequences_dtf.sequence]
unlinked_sequences_dtf.sequence_text.value_counts().head(20)


# %%


polities_dtf[polities_dtf.typology.apply(lambda t: t is None)].hds_tag.value_counts()


# ### Statusword-toponyms + single toponyms linking results

# %%


single_toponyms_sequences_dtf.head()


# %%


#valid_sequences_dtf.head()
valid_sequences_dtf[[len(t)>1 for t in valid_sequences_dtf.toponym_tokens_spans]][
    ["toponym_tokens_spans", "sequence", "sequence_toponym", 
    "linked_polity_id", 'linked_hds_tag', 'linked_toponym']
].head()


# %%


statusword_toponyms_columns = list(valid_sequences_dtf.columns)
single_toponyms_columns = list(single_toponyms_sequences_dtf.columns)

sw_columns = [c for c in statusword_toponyms_columns if c not in single_toponyms_columns]
otop_columns = [c for c in single_toponyms_columns if c not in statusword_toponyms_columns]
common_columns = [c for c in single_toponyms_columns if c in statusword_toponyms_columns]


print("Only statusword-toponym columns:", sw_columns,"\n")
print("Only single toponym columns:", otop_columns,"\n")
print("common columns:", common_columns,"\n")

# -> columns to keep from valid_sequences_dtf are 'statusword', 'sequence'
statusword_columns_to_keep= ['statusword', 'sequence']
linked_toponyms_columns = [
    c for c in statusword_toponyms_columns
    if c in single_toponyms_columns or c in statusword_columns_to_keep
]


# ### Putting together all the identified polities mentions

# %%


for c in statusword_columns_to_keep:
    single_toponyms_sequences_dtf[c] = None

all_identified_polities = pd.concat([
    valid_sequences_dtf[linked_toponyms_columns],
    single_toponyms_sequences_dtf[linked_toponyms_columns]
])
print("Verification that we have the same nb of entries in toponyms_dtf and all_identified_polities:")
print("- nb entries in toponyms_dtf: ",toponyms_dtf.shape[0])
print("- nb entries in all_identified_polities: ", all_identified_polities.shape[0])
print("- nb of duplicate entries in all_identified_polities: ", all_identified_polities.toponym_tokens_spans.duplicated().sum())


# %%



all_identified_polities_spans = set(all_identified_polities.toponym_tokens_spans)
missing_toponyms = toponyms_dtf[toponyms_dtf.toponym_tokens_spans.apply(lambda tts:
    tts not in all_identified_polities_spans
)]
missing_toponyms.head()


# %%


missing_toponyms_spans = set(missing_toponyms.toponym_tokens_spans)

statusword_tokens_sequences_dtf[statusword_tokens_sequences_dtf.toponym_tokens_spans.apply(lambda tts:
    tts  in missing_toponyms_spans
)].shape


# %%


non_analysable_sequences_dtf.shape


# ## Annotating linked polities in documents

# %%


def add_annotation_to_document_from_valid_sequences(document, valid_sequences_dtf_rows):
    new_annotations = [
        Annotation(
            row.toponym_tokens_spans[0].idx,
            row.toponym_tokens_spans[-1].idx+len(row.toponym_tokens_spans[-1]),
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
    add_annotation_to_document_from_valid_sequences(row.document, all_identified_polities[all_identified_polities.hds_article_id==row.hds_article_id])


# %%


# COMPLETING ANNOTATIONS OF MULTI-TOKEN TOPONYMS
sampled_articles_dtf.iloc[32,:].hds_article_id

all_identified_polities[all_identified_polities.hds_article_id=="001245"]
dtf_row = all_identified_polities[all_identified_polities.hds_article_id=="001245"].iloc[1,:]

all_identified_polities[all_identified_polities.hds_article_id=="001245"].iloc[0,:].possible_polities

#hds_tag = valid_sequences_dtf.loc[valid_sequences_dtf.hds_article_id=="001245",["hds_tag"]]


# %%


test_values = [
    valid_sequences_dtf.shape[0],      statusword_tokens_sequences_dtf.shape[0]
]
truth_sequence = [
    valid_sequences_dtf.shape[0]==727, statusword_tokens_sequences_dtf.shape[0]==1456
]

print(all(truth_sequence))
print(test_values)
print(truth_sequence)


# %%


test = linked_sequences_dtf.merge(polities_dtf.loc[:,["polity_id", "tokenized_toponym_texts"]], left_on="linked_polity_id", right_on="polity_id", how="left")
test.tokenized_toponym_texts.apply(len).value_counts()


# %%


all_identified_polities.shape


# %%


[a for a in sampled_articles_dtf.document.iloc[0].annotations]


# %%




