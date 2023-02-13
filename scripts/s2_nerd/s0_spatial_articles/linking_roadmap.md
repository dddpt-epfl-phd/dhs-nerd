

# Polity linking strategy

## Needs

- taking an arbitrary char_span and linking it
- disambiguating polities with the same toponym
- marking ambiguous matches
- finding measures of success
- handling alternative names for polities (from the DHS+multilinguals)

## Challenges

- not bloating the architecture
- handling ambiguous matches?
    -> keeping a "toponym" class of entity (with the corresponding possible final polities)

### limitations/bugs of the rule-based approach

- analyse_statuswords_toponyms_sequences()/analyse_statusword_tokens_sequence_single()
    -> labels tokens as "TOPONYM" if the token.text is part of the pre-defined list of tokens existing in polities_dtf toponyms
    -> "TOPONYM" status should only be derived from the recognized entity mention

## Propositions:

1) adapt the HF output to the dtf rule-based pipeline format
+ faster
+ will work
- current rule-based linking might be totally faaalse

2) adapt the pipeline to be more "generic"/"robust"
+ might obtain more generic pipeline
- generalization of specialized code: doesn't make much sense
- what about other more serious approaches of linkings

-> choose option 1)

## TODO

steps to link entities from HF output
- add HF output to articles_dtf in a coherent manner
- adapt HF output to dtf format
    -> must mimick output of add_text_toponyms_spans(), ready to be ingested in to_toponyms_dtf()
    - columns needed:
        + toponym_tokens_spans: list of spacy.Span of the recognized entities
        + tokenized_toponym: the spacy.Tokens of the identified mention needed by
            ~ normalize_toponyms() on the dtf
- link them using spatial_articles_utils.py
- create new larger function doing all the steps starting from a properly formatted dtf
- refactoring to better linkining HF+rule-based outputs
- from the spatial_articles_utils.-py back to a json format
- display HF vs rule-based results using comparePredTrue

### 1) adapt HF output to dtf format

steps:
1) starting from a dtf-row for an article
    - do HF recognition
    - transform HF back to a spacy.Doc+spacy.Token representation
    - do linking
        + handle case where entity not included in linking




# Functions

- DONE text_block_entity_recognition(): Does the Named entity recognition on a given text, if given a text_block annotation, shifts the start-end accordingly
- DONE document_text_blocks_entity_recognition(): does the NER on a given Document
    + adds annotations corresponding to the ner_results
    + returns a single ner_results list corresponding to the whole document text
- DONE articles_dtf_entity_recognition(): does the entity-recognition on the articles, using document_text_blocks_entity_recognition()
    + adds the following columns:
        - ner_results: list of ner results from the hf pipeline (per hf-text-block of the max length accepted by the hf pipeline)
        + toponym_tokens_spans: list of spacy.Span of the recognized entities

# Misc


[the fuzz: great levenstein distance py library](https://github.com/seatgeek/thefuzz)



