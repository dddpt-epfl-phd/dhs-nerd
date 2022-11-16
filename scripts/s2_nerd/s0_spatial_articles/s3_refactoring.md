# Propositions to improve code quality
Status:
- we're working with dataframes (articles, polities, sequences)
- we have a few functions but lots of things happen outside functions
- some dtf columns are implicitly expected according to which function/cell you are running
- quite a few intermediary dtf with unclear column names

Proposition:
- make a sequence of functions starting from polities_dtf/articles_dtf
- make a few "master" functions calling the proper sequence of single functions
- weed out as much of the code as possible from outside the functions
- explitlify expected dataframe columns 

## Functions:
### tokenization & preprocessing
- add_tokenized_text(): takes a dtf with "text" column
    + adds the following columns:
        - tokens: spacy tokenization of text column
- add_toponyms(): takes a dtf with a "toponym" column
    + adds the following columns:
        - tokenized_toponym: spacy tokenization texts of toponym
- normalize_toponyms(): takes a dtf coming from add_toponyms()
    + adds the following columns:
        - loose_normalized_tokenized_toponym: all toponym tokens that are generally toponym (exlcuding "les", "la", etc...)
        - strict_normalized_tokenized_toponym: same as loose_normalized_tokenized_toponym, excluding in addition ambiguous toponym tokens ("eaux", "ile", "bois", "col", etc...)
    + returns:
        - normalized_toponym_tokens: set of all strict_normalized_tokenized_toponym
- is_token_toponym(): checks whether an article's token is a toponym token based on:
    + normalized_toponym_tokens
    + the current article's loose_normalized_tokenized_toponym
- add_toponym_tokens_sequences(): takes nb_predecessors, nb_successors and a dtf coming from add_toponyms() and add_tokenized_text()
    /!\ current implementation ignores some toponym_tokens (see challenges) /!\
    + adds the following columns:
        - toponym_tokens: tokens from the text that are identified as a toponym 
        - toponym_sequence_tokens: for each toponym_token, a sequence according from nb_pred to nb_succ
    /!\ current implementation ignores some toponym_tokens (see challenges) /!\
### polity recognition
- identify_statuswords_toponyms_sequences(): takes a dtf coming from add_toponym_tokens_sequences()
    + returns a new dtf statusword_tokens_sequences_dtf with one row per sequence containing at least 1 statusword and 1 toponym
- explode_statuswords_toponyms_sequences(): takes a dtf coming from identify_statuswords_toponyms_sequences()
    + returns a new dtf sequences_analyses_dtf (renaming it tostatusword_tokens_sequences_dtf?) with one row per statusword+toponym combination (multiple rows possible for one toponym sequence)
- validate_statuswords_toponyms_sequences(): takes valid_sequence_structures set of strings and a dtf coming from explode_statuswords_toponyms_sequences()
    + returns a new dtf valid_sequences_dtf containing the valid statuswords_toponyms_sequences
### polity linking
- link_entity_by_hdstag() already exists
- link_statuswords_toponyms_sequences() takes a dtf coming from validate_statuswords_toponyms_sequences()
    + adds columns
        - possible_polities
        - possible_polities_min_rank
        - linked_polity_id, linked_hds_tag, linked_toponym
### annotating back documents 
- add_annotation_to_document_from_valid_sequences() already exists

# Next steps

### Polity recognition and linking for toponyms without statuswords

# Challenges

### creation of `sampled_articles_dtf["toponym_tokens"]`
- ignores first token of text
- only identifies first token of a toponym tokens sequence