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
- DONE add_tokenized_text(): takes a dtf with "text" column
    + adds the following columns:
        - tokens: spacy tokenization of text column
- DONE add_toponyms(): takes a dtf with a "toponym" column
    + adds the following columns:
        - tokenized_toponym: spacy tokenization texts of toponym
- DONE normalize_toponyms(): takes a dtf coming from add_toponyms()
    + adds the following columns:
        - loose_normalized_tokenized_toponym: all toponym tokens that are generally toponym (exlcuding "les", "la", etc...)
        - strict_normalized_tokenized_toponym: same as loose_normalized_tokenized_toponym, excluding in addition ambiguous toponym tokens ("eaux", "ile", "bois", "col", etc...)
        - trimmed_normalized_tokenized_toponym: removing leading tokens that are not_toponym_tokens (mainly to avoid confusion with regard to toponyms such as "Les Verrières")
    + returns:
        - normalized_toponym_tokens: set of all strict_normalized_tokenized_toponym
- DONE add_text_toponyms_spans():  takes a dtf coming from normalize_toponyms()
    + adds the following columns: 
        - toponym_tokens_spans: list of spacy Spans, each Span containing a toponym, ensures no overlaps
- DONE save_toponym_tokens_spans(): takes a dtf coming from add_text_toponyms_spans()
    - save the toponym_tokens_spans column to a pickle
- DONE restore_toponym_tokens_spans(): restores the toponym_tokens_spans column from pickle 
- DONE restore_or_compute_and_save_toponym_spans()
- DONE to_toponyms_dtf(): takes a dtf coming from add_text_toponyms_spans()
    + returns a dtf with one line per toponym span
- TODO add_toponym_tokens_sequences(): takes nb_predecessors, nb_successors and a dtf coming from add_text_toponyms_spans() and add_tokenized_text()
    + adds the following columns:
        - toponyms_tokens_sequences: for each toponym_token_span, a sequence according from nb_pred to nb_succ (indexed on first token from each span)

### polity recognition
- TODO identify_statuswords_toponyms_sequences(): takes a dtf coming from add_toponym_tokens_sequences()
    + adds a column "statusword_tokens_sequences" to dtf containing all the toponyms_tokens_sequences also containing a statusword
    + returns a new dtf statusword_tokens_sequences_dtf with one row per sequence containing at least 1 statusword and 1 toponym
- DONE analyse_statuswords_toponyms_sequences(): takes a dtf coming from identify_statuswords_toponyms_sequences()
    + returns a new dtf sequences_analyses_dtf (renaming it to statusword_tokens_sequences_dtf?) with one row per statusword+toponym combination (multiple rows possible for one toponym sequence)
- DONE validate_statuswords_toponyms_sequences(): takes valid_sequence_structures set of strings and a dtf coming from explode_statuswords_toponyms_sequences()
    + returns a new dtf valid_sequences_dtf containing the valid statuswords_toponyms_sequences
### polity linking
- DONE link_entity_by_hdstag() already exists
- DONE link_statuswords_toponyms_sequences() takes a dtf coming from validate_statuswords_toponyms_sequences()
    + adds columns
        - possible_polities
        - possible_polities_min_rank
        - linked_polity_id, linked_hds_tag, linked_toponym
### annotating back documents 
- (DONE) add_annotation_to_document_from_valid_sequences() already exists

# Next steps

### Polity recognition and linking for toponyms without statuswords


needs:
- detect toponyms that are without statusword
- don't double detect toponyms that have a statusword
    - properly identify multi-tokens toponyms

proposition:
- re-detect all toponyms
- ignore toponyms that are in a 

## NEXT TIME

Use [spacy's rule-based matching](https://spacy.io/usage/rule-based-matching#adding-patterns) from the start!

