
# %%
import unicodedata
import spacy

from s2_prepare_articles import *


# %%
spacy_tokenizer = spacy.load("fr_core_news_sm")



# %% Evaluating normalized text difference with original text:

polities_dtf["normalized_text"] = polities_dtf.document.apply(lambda d: unicodedata.normalize("NFKC",d.text))

polities_dtf["len_normalized_text"] = polities_dtf["normalized_text"].apply(len)
polities_dtf["len_unnormalized_text"] = polities_dtf.document.apply(lambda d: len(d.text))
polities_dtf["len_diff_normalized_text"] = polities_dtf["len_unnormalized_text"] - polities_dtf["len_normalized_text"]
polities_dtf["len_diff_normalized_text"].value_counts()

# %% Character normalization investigation -> NFKC is the way to go :-)

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

[investigate_norm_len_diff(lendifNFKC, i) for i in range(2)]


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
- frequency table of 5 predecessor words
    -> identify the relevant ones


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
 'près',
 'sur',
 'zum'
}
ambiguous_toponym_tokens={
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

# toponym_tokens: tokens in the text that denote a toponym
sampled_articles_dtf["toponym_tokens"] = [
    # handle the case of multiple toponym tokens: in this case only take first token each time
    [
        token for token in row.tokens
        if token.text in normalized_toponym_tokens
        or token.text in row.loose_normalized_tokenized_toponym
        and (token.i==0 or token.nbor(-1).text not in row.tokenized_toponym)
    ]
    for k, row in sampled_articles_dtf.iterrows()
]

# %%

nb_predecessors = 10
nb_successors = 1
sampled_articles_dtf["predecessors_tokens"] = [
    [t.nbor(i) for t in row.toponym_tokens for i in range(-min(nb_predecessors,t.i),nb_successors+1)]
    for k, row in sampled_articles_dtf.iterrows()
]
predecessors_tokens = sampled_articles_dtf["predecessors_tokens"].apply(lambda ts: [t.text for t in ts]).explode()
predecessors_tokens_value_counts = predecessors_tokens.value_counts().to_frame()

# %%

#pd.set_option('display.max_rows', None)
predecessors_tokens_value_counts[predecessors_tokens_value_counts.predecessors_tokens==2]

statusword_token_text = [
    # > 4 appearances
    "seigneur",
    "région",
    "abbaye",
    "canton",
    "château",
    #"terres",
    "district",
    "communes",
    "village",
    "seigneurie",
    "bailliage",
    "commune",
    "paroisse",
    "ville",
    # 3 appearances
    "dîme", # -> ?
    "hameau",
    #"vestiges",# -> ?
    "communauté",
    "Commune",
    #"hôpital",
    "villages",
    "seigneurs",
    "communautés",
    # 2
    "suzeraineté",
    "administration",
    "circonscriptions",
    "bourgade",
    "juridictions",
    "localités",
    "cercle",
    "Munizipalgemeinde",
    "Ortsgemeinden",
    "vallon",
    "chapitre",
    "dîmes", # -> ?
    "juridiction",
    "prieuré",
    "abbés",
    "abbé",
    "évêque",
    "châtellenie",
]
# %%

sampled_articles_dtf["toponyms_tokens_sequences"] = [
    [
        [t.nbor(i) for i in range(-min(nb_predecessors,t.i),nb_successors+1)]
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
    [seq for seq in toponyms_tokens_sequences if any(token.text in statusword_token_text for token in seq)]
    for toponyms_tokens_sequences in sampled_articles_dtf.toponyms_tokens_sequences
]
# %%

statusword_tokens_sequences = [
    seq for statusword_tokens_sequences in sampled_articles_dtf.statusword_tokens_sequences
    for seq in statusword_tokens_sequences
]

# %%

def analyse_statusword_tokens_sequence_single(dtf_row, token_sequence, statusword_index, toponym_index):
    """"""
    sequence = token_sequence[statusword_index:(toponym_index+1)]
    sequence_structure = [
        "STATUS" if token.text in statusword_token_text else(
        "TOPONYM" if (
            token.text in normalized_toponym_tokens or token.text in dtf_row.loose_normalized_tokenized_toponym
        ) else token.text
        )
        for token in sequence
    ]
    statusword = token_sequence[statusword_index]
    return (statusword, sequence, sequence_structure)

def analyse_statusword_tokens_sequence(dtf_row, token_sequence):
    """
    Goals:
    1) find statusword token
    2) trim down sequence from statusword-token to toponym token
    3) get a structureal-token sequence "status-XX-toponym"
    """
    statusword_indices = [i for i,tok in enumerate(token_sequence) if tok.text in statusword_token_text]
    toponym_indices = [i for i,tok in enumerate(token_sequence) if tok.text in normalized_toponym_tokens or tok.text in dtf_row.loose_normalized_tokenized_toponym]
    sequences_analyses = [
        analyse_statusword_tokens_sequence_single(dtf_row, token_sequence, i, j)
        for i in statusword_indices for j in toponym_indices[:1] if i<j # only consider first toponym_index
    ]
    return sequences_analyses

# %%
statusword_tokens_sequences_dtf = sampled_articles_dtf.explode("statusword_tokens_sequences")
statusword_tokens_sequences_dtf = statusword_tokens_sequences_dtf[['hds_article_id', 'toponym', 'geoidentifier', 'article_title', 'polities_ids', 'nb_polities',
       'tokenized_toponym', 'loose_normalized_tokenized_toponym',
       'strict_normalized_tokenized_toponym',
       'statusword_tokens_sequences']].copy()
# %%
statusword_tokens_sequences_dtf["sequence_analysis"] = [
    analyse_statusword_tokens_sequence(row, row.statusword_tokens_sequences)
    for k, row in statusword_tokens_sequences_dtf.iterrows()
]

# %%

sequences_analyses_dtf = statusword_tokens_sequences_dtf.explode("sequence_analysis")
sequences_analyses_dtf = sequences_analyses_dtf[~sequences_analyses_dtf.sequence_analysis.isna()]
sequences_analyses_dtf["statusword"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[0])
sequences_analyses_dtf["sequence"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[1])
sequences_analyses_dtf["sequence_structure"] = sequences_analyses_dtf.sequence_analysis.apply(lambda sa: sa[2])
sequences_analyses_dtf["sequence_structure_str"] = sequences_analyses_dtf["sequence_structure"].apply(lambda ss: "-".join(ss))
sequence_structures = sequences_analyses_dtf["sequence_structure_str"].value_counts()

# %%

sequence_structures
sequence_structures[sequence_structures>5].shape

# %%

sequence_structures_human_columns = ['toponym', 'article_title', 'polities_ids', "statusword", "sequence", "sequence_structure"]

sequence_structure = "STATUS-(-TOPONYM"
sequences_analyses_dtf.loc[sequences_analyses_dtf["sequence_structure_str"]==sequence_structure,sequence_structures_human_columns]
# %%


