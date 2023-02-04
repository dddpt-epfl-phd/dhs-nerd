import re
import unicodedata

from tqdm import tqdm 
import pandas as pd

def normalize_unicode_text(text):
    """unicode normalization NFKD removes accents in characters -> NFKC is the way to go :-)
    
        /!\\ /!\\ /!\\ normalizing text yields different text lengths for 3 articles (out of 4000), use with caution /!\\/!\\/!\\
        but it is needed for proper tokenization/prediction/learning"""

    return unicodedata.normalize("NFKC",text)

def add_tokenized_text(dtf, tokenizer):
    """
    takes a dtf with "document" column
    + adds the following columns:
        - tokens: spacy tokenization of text column
    """
    dtf["tokens"] = dtf.document.apply(lambda d: tokenizer(normalize_unicode_text(d.text)))
    return dtf

def add_toponyms(dtf, tokenizer):
    """
    takes a dtf with a "toponym" column
    + adds the following columns:
        - tokenized_toponym: spacy tokenization texts of toponym
    """
    dtf["tokenized_toponym"] = [tokenizer(t) for t in tqdm(dtf.toponym, total=dtf.shape[0], desc="Tokenizing toponyms")]


def normalize_toponyms(dtf, not_toponym_tokens_texts, ambiguous_toponym_tokens_texts):
    """
    normalize_toponyms(): takes a dtf coming from add_toponyms()
    + adds the following columns:
        - loose_normalized_tokenized_toponym: all toponym tokens that are generally toponym (exlcuding "les", "la", etc...)
        - strict_normalized_tokenized_toponym: same as loose_normalized_tokenized_toponym, excluding in addition ambiguous toponym tokens ("eaux", "ile", "bois", "col", etc...)
        - trimmed_normalized_tokenized_toponym: removing leading tokens that are not_toponym_tokens (mainly to avoid confusion with regard to toponyms such as "Les Verrières")
    + returns:
        - normalized_toponym_tokens: set of all strict_normalized_tokenized_toponym
    """
    dtf["trimmed_normalized_tokenized_toponym"] = [
        [s for s in tokens[:1] if s.text not in not_toponym_tokens_texts]+
        [t for t in tokens[1:]]
        for tokens in dtf["tokenized_toponym"]
    ]   
    dtf["loose_normalized_tokenized_toponym"] = [[s.text for s in tokens if s.text not in not_toponym_tokens_texts] for tokens in dtf["tokenized_toponym"]]
    dtf["strict_normalized_tokenized_toponym"] = [[st for st in texts if st not in ambiguous_toponym_tokens_texts] for texts in dtf["loose_normalized_tokenized_toponym"]]
    normalized_toponym_tokens = set(dtf["strict_normalized_tokenized_toponym"].explode())
    trimmed_normalized_tokenized_toponyms_texts = [t for t in dtf["trimmed_normalized_tokenized_toponym"].apply(lambda tokens: "".join([t.text+t.whitespace_ for t in tokens])) if len(t)>0]
    return normalized_toponym_tokens, trimmed_normalized_tokenized_toponyms_texts


def is_token_toponym(token, dtf_row, normalized_toponym_tokens):
    """Checks that a given token is a toponym (either corresponding to any strict toponym, or a loose toponym from the particular article toponym
    """
    return (
        token.text in normalized_toponym_tokens
        or token.text in dtf_row.loose_normalized_tokenized_toponym
    )


def add_text_toponyms_spans(dtf, trimmed_normalized_tokenized_toponyms_texts):
    """add_text_toponyms_spans():  takes a dtf coming from normalize_toponyms()
    + adds the following columns: 
        - toponym_tokens_spans: list of spacy Spans, each Span containing a toponym, ensures no overlaps

    algorithm:
    The pattern requires whitespace before&after toponym,
    hence we add whitespace at beginning and end of text to ensure detection at those places
    and correct match indices afterwards
    
    example:
    real text:
    "MEIERKAPPEL, BLABLA"	    -> real bounds 0, 11
    with added space:
    " MEIERKAPPEL, BLABLA" -> displaced bounds 1, 12
    detected:
    " MEIERKAPPEL,"         -> detected bounds 0, 13

    real_start = m.start()+1-1, +1 because \W in pattern, -1 because " " added in front of text
    real_end = m.end()-2 because \W at start and end of pattern
    
    """

    toponyms_pattern = re.compile("("+(r")\W|\W(".join(trimmed_normalized_tokenized_toponyms_texts))+")")

    # multi-tokens toponyms
    dtf["toponym_tokens_spans"]=[
        [
            row.tokens.char_span(m.start(), m.end()-2, alignment_mode="contract")
            for m in toponyms_pattern.finditer(" "+row.document.text+" ") #, re.IGNORECASE):
        ]
        for i, row in tqdm(dtf.iterrows(), total = dtf.shape[0], desc ="Adding token spans")
    ]
    dtf["toponym_tokens_spans"] = dtf["toponym_tokens_spans"].apply(lambda spans: [s for s in spans if s is not None])
    dtf["toponym_tokens_indices"] = dtf["toponym_tokens_spans"].apply(lambda spans: set([t.i for span in spans for t in span]))

    # single token toponyms that are in the row.loose_normalized_tokenized_toponym (think "Au", "le Pont", "See", etc...)
    dtf["toponym_tokens_spans"] = [
        row.toponym_tokens_spans+
        [
            row.tokens[token.i:(token.i+1)] for token in row.tokens
            if 
                token.i not in row.toponym_tokens_indices and # ensure we don't have twice the same toponyms
                token.text in row.loose_normalized_tokenized_toponym
        ]
            for i, row in dtf.iterrows()
    ]
    del dtf["toponym_tokens_indices"]
        


def add_toponym_tokens_sequence(dtf, nb_predecessors = 10, nb_successors = 3):
    """add_toponym_tokens_sequence(): takes nb_predecessors, nb_successors and a dtf coming from add_text_toponyms_spans() and add_tokenized_text()
    + adds the following columns:
        - toponym_tokens_sequence: for each toponym_token_span, a sequence according from nb_pred to nb_succ (indexed on first token from each span)"""

    dtf["toponym_tokens_sequence"] = dtf.toponym_tokens_spans.apply(lambda span: [
        span[0].nbor(i)
        for i in range(
            -min(nb_predecessors,span[0].i),
            min(nb_successors, len(span[0].doc)-span[0].i)
        )
    ])


def identify_statusword_toponym_sequences(dtf, statuswords_text):
    """
    takes a dtf coming from add_toponym_tokens_sequence()
    + adds a column "toponym_tokens_sequence" to dtf containing all the toponym_tokens_sequence also containing a statusword
    + returns a new dtf statusword_tokens_sequences_dtf with one row per sequence containing at least 1 statusword and 1 toponym
    """
    dtf["is_statusword_toponym_sequence"] = [
            any(token.text.lower() in statuswords_text for token in seq)
            for seq in dtf.toponym_tokens_sequence
    ]



def analyse_statusword_tokens_sequence_single(dtf_row, token_sequence, statusword_index, toponym_index, statuswords_text, normalized_toponym_tokens):
    """Analyses a single statusword-toponym combination

    returns a sequence whose first term is the sequence's statusword, and the last word is the sequence's toponym
    """
    sequence = token_sequence[statusword_index:(toponym_index+1)]
    sequence_structure = [
        "STATUS" if token.text.lower() in statuswords_text else(
        "TOPONYM" if is_token_toponym(token, dtf_row, normalized_toponym_tokens)
        else token.text
        )
        for token in sequence
    ]
    statusword = token_sequence[statusword_index]
    toponym = token_sequence[toponym_index]
    return (statusword, toponym, sequence, sequence_structure)

def analyse_statusword_tokens_sequence(dtf_row, token_sequence, statuswords_text, normalized_toponym_tokens):
    """Returns all the possible statusword-toponym combination analyses for a given token sequence
    """
    statusword_indices = [i for i,tok in enumerate(token_sequence) if tok.text.lower() in statuswords_text]
    #toponym_indices = [i for i,tok in enumerate(token_sequence) if tok.text in normalized_toponym_tokens or tok.text in dtf_row.loose_normalized_tokenized_toponym]
    toponym_indices = [i for i, t in enumerate(token_sequence) if t.i == dtf_row.toponym_tokens_spans[0].i]
    #toponym_indices = [len(token_sequence)-nb_successors] # the toponym is always at the same spot in the sequence
    sequences_analyses = [
        analyse_statusword_tokens_sequence_single(dtf_row, token_sequence, i, j, statuswords_text, normalized_toponym_tokens)
        for i in statusword_indices for j in toponym_indices if i<j
    ]
    return sequences_analyses


def validate_statuswords_toponyms_sequences(dtf, valid_sequence_structures):
    """
    takes valid_sequence_structures set of strings and a dtf coming from explode_statuswords_toponyms_sequences()
    + returns a new dtf valid_sequences_dtf containing the valid statuswords_toponyms_sequences
    """
    valid_sequences_indexes = dtf.sequence_structure_str.apply(lambda struct: struct in valid_sequence_structures)
    valid_sequences_dtf = dtf[valid_sequences_indexes].copy()
    invalid_sequences_dtf = dtf[~valid_sequences_indexes].copy()
    return valid_sequences_dtf, invalid_sequences_dtf



def reintegrate_dtf(dtf_to_reintegrate, mother_dtf, dtfs_to_check_against=[]):
    """reintegrates a dtf_to_reintegrate inside a mother_dtf,
    checking for toponym_tokens_spans duplicates inside both mother_dtf and dtfs_to_check_against"""
    shape0 = dtf_to_reintegrate.shape[0]
    dtf_to_reintegrate_kept_rows = dtf_to_reintegrate[
        ~dtf_to_reintegrate.toponym_tokens_spans.duplicated()
    ]
    shape1 = dtf_to_reintegrate_kept_rows.shape[0]
    print("Duplicates removed:", shape0-shape1)
    existing_toponym_tokens_spans = set(
        [s for dtf in dtfs_to_check_against for s in dtf.toponym_tokens_spans] +
        [s for s in mother_dtf.toponym_tokens_spans]
    )
    dtf_to_reintegrate_kept_rows = dtf_to_reintegrate_kept_rows[[
        s not in existing_toponym_tokens_spans
        for s in dtf_to_reintegrate_kept_rows.toponym_tokens_spans
    ]]
    shape2 = dtf_to_reintegrate_kept_rows.shape[0]
    print("toponym_tokens_spans removed as already present in other dtfs:", shape1-shape2)
    print(shape2, "entries reintegrated, from the", shape0, "present in original dtf_to_reintegrate")
    return pd.concat([
        mother_dtf,
        dtf_to_reintegrate_kept_rows[mother_dtf.columns]
    ])




def create_toponyms_exact_match_dict(polities_dtf, default_hdstag_priorization):
    default_hdstag_priorization_dict = {t:i for i,t in enumerate(default_hdstag_priorization)}
    toponyms_exact_match_dict = {}
    for i, row in polities_dtf.iterrows():
        toponym_key = "".join([t.text+t.whitespace_ for t in row.trimmed_normalized_tokenized_toponym])
        toponym_possible_polities = toponyms_exact_match_dict.get(toponym_key)
        if toponym_possible_polities is None:
            toponyms_exact_match_dict[toponym_key] = [None]*len(default_hdstag_priorization_dict)
            toponym_possible_polities = toponyms_exact_match_dict[toponym_key]
        hdstag_priorization = default_hdstag_priorization_dict.get(row.hds_tag)
        if hdstag_priorization is not None:
            # if it has a priorization: put it in its proper priorization position
            toponym_possible_polities[hdstag_priorization] = row.polity_id
        else: 
            # else append it at the end
            toponym_possible_polities.append(row.polity_id)

    for k,v in toponyms_exact_match_dict.items():
        # remove None entries from the priorization:
        toponyms_exact_match_dict[k] = [pid for pid in v if pid is not None]

    #pd.Series([len(v) for v in toponyms_exact_match_dict.values()]).value_counts()
    return toponyms_exact_match_dict


def link_toponym_by_exact_match(toponym, toponyms_exact_match_dict):
    """Links a single toponym to its possible polities by toponym exact match
    """
    possible_polities= toponyms_exact_match_dict.get(toponym)
    return possible_polities if possible_polities is not None else []

def link_single_toponyms(dtf, polities_dtf, toponyms_exact_match_dict):
    """
    link_single_toponyms(): takes a dtf coming from identify_statusword_toponym_sequences()
    + links single toponyms to the polity ids found in the result from create_toponyms_exact_match_dict()
    + adds columns
        - possible_polities
        - linked_polity_id, linked_hds_tag, linked_toponym
    """
    dtf["possible_polities"] = dtf.toponym_tokens_spans.apply(lambda span:
        link_toponym_by_exact_match(span.text, toponyms_exact_match_dict)
    )
    dtf["linked_polity_id"] = [(pp[0] if len(pp)>0 else None) for pp in dtf["possible_polities"]]
    dtf["linked_hds_tag"] = [(polities_dtf.hds_tag[polities_dtf.polity_id==lpi].iloc[0] if lpi is not None else None) for lpi in dtf["linked_polity_id"]]
    dtf["linked_toponym"] = [(polities_dtf.toponym[polities_dtf.polity_id==lpi].iloc[0] if lpi is not None else None) for lpi in dtf["linked_polity_id"]]




def count_nb_matching_tokens(sequence_dtf_row, tokenized_toponym_texts):
    sequence_dtf_row_tokens_texts = [t.text for t in sequence_dtf_row.toponym_tokens_sequence]
    nb_matching_tokens = sum([
        word in sequence_dtf_row_tokens_texts#[-(nb_successors+1):]
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

def link_statuswords_toponyms_sequences(dtf, polities_dtf, statusword_to_hdstag_dict):
    """
    takes a dtf (valid_sequences_dtf) coming from validate_statuswords_toponyms_sequences()
    + adds columns
        - possible_polities
        - possible_polities_min_rank
        - linked_polity_id, linked_hds_tag, linked_toponym
    """
    dtf["possible_polities"] = [
        link_entity_by_hdstag(row, polities_dtf, statusword_to_hdstag_dict)
        for i, row in tqdm(dtf.iterrows(), total=dtf.shape[0], desc="Linking entities by HDS tag")
    ]

    #valid_sequences_dtf["possible_polities_ranks"] = valid_sequences_dtf["possible_polities"].apply(lambda pp: [t[0] for t in pp])
    dtf["possible_polities_min_rank"] = dtf["possible_polities"].apply(lambda pp_dtf: pp_dtf.possibility_hds_tag_rank.min() if pp_dtf.shape[0]>0 else None)

    dtf["linked_polity_id"] = dtf["possible_polities"].apply(lambda pp: pp.iloc[0]["polity_id"] if pp.shape[0]>0 else None)
    dtf["linked_hds_tag"] = dtf["possible_polities"].apply(lambda pp: pp.iloc[0]["hds_tag"]if pp.shape[0]>0 else None)
    dtf["linked_toponym"] = dtf["possible_polities"].apply(lambda pp: pp.iloc[0]["toponym"]if pp.shape[0]>0 else None)




