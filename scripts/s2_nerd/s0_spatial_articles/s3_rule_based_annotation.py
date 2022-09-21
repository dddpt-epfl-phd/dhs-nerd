
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
nb_successors = 1
sampled_articles_dtf["predecessors_tokens"] = [
    [t.nbor(i) for t in row.toponym_tokens for i in range(-min(nb_predecessors,t.i),nb_successors+1)]
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
    toponym_indices = [len(token_sequence)-nb_successors-1] # the toponym is always at the same spot in the sequence
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

{t: [] for t in set(polities_dtf.typology)}

# %%







polities_dtf[polities_dtf.typology=="baillage"]

# %%



statusword_to_typology_dict = {
    # lordships
    (
        "seigneur",
        "seigneurs",
        "seigneurie",
        "seigneuries",
    ) : ["seigneurie", "châtellenie", "duché", "mandement", "commanderie"],
    (
        "châtellenie",
        "châtellenies",
    ) : ["châtellenie", "seigneurie"],
    (
        "mandement",
        "mandements"
    ) : ["mandement", "seigneurie"],
    (
        "comte",
        "comtes",
        "comté",
        "comtés",
    ) : ["comté", "seigneurie"],
    (
        "baron",
        "barons",
        "baronnie",
        "baronnies",
    ) : ["baronnie", "seigneurie"],
    (
        "duc",
        "ducs",
        "duché",
        "duchés",
    ) : ["duché", "seigneurie"],
    (
        # cantons
        "canton",
        "cantons",
    ) : ["canton", 'état'],
    (
        # administrative: district/bailliage/etc
        "district",
        "districts",
        "distr",
    ) : ["district", 'pieve', 'gouvernement'],
    (
        "dizain",
        "dizains"
    ) : ["dizain", "bailliage"],
    (
        "pieve"
    ) : ["pieve", "bailliage"],
    (
        "bailliage",
        "bailliages",
        "bailli",
        "baillis",
    ) : ["bailliage", "baillage"],
    (
        'gouvernement',
        'gouvernements'
    ) : ['gouvernement', "bailliage"],
    (
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
        "hameau",
        "hameaux",
        "paroisse",
        "paroisses",
        "bourgade",
        "bourgades",
        "localité",
        "localités",
    ) : ["commune", 'village', "localité"],
    (
        "ville",
    ) : ['ville', "canton", "commune", 'état'],
    (
        # ecclesiastical
        "chapitre",
    ) : ["chapitre", 'chapitre collégial', 'abbaye/couvent/monastère/prieuré'],
    (
        "prieuré",
        "prieurés",
    ) : ["prieuré", 'abbaye/couvent/monastère/prieuré'],
    (
        "abbaye",
        "abbayes",
        "abbé",
        "abbés",
    ) : ["abbaye", 'abbaye de bénédictines', 'abbaye de bénédictins', 'principauté abbatiale', 'abbaye/couvent/monastère/prieuré'],
    (
        "évêque",
        "évêques",
        "évêché",
        "évêchés",
    ) : ["évêché"],
    (
        "diocèse",
        "diocèses",
    ) : ["évêché"],
    (
        "archevêque",
        "archevêques",
        "archevêché",
        "archevêchés"
    ) : ["archidiocèse"],
    (
        "archidiocèse",
        "archidiocèses",
    ) : ["archidiocèse"],
    (
        "monastère",
        "monastères",
    ) : ['abbaye/couvent/monastère/prieuré'],
    (
        'couvent',
        'couvents'
    ) : ['couvent', 'abbaye/couvent/monastère/prieuré'],
    ( # quite special as an avouerie is a military protect of a ecclesiastical entity
        "avouerie",
        "avoueries",
    ) : [], # ["duché"]
    (
        'prévôté',
        'prévôtés',
    ) : ['prévôté', 'abbaye/couvent/monastère/prieuré'],
    (
        "commanderie",
        "commanderies",
    ) : ["commanderie"],
    (
        # fuzzy terms
        "région",
        "régions",
        "domaine",
        "domaines",
        "vallon",
        "administration",
        "circonscriptions",
        "cercle",
        "cercles",
    ) : []
}