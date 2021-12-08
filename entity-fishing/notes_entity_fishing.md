
# Pre-annotate data with entity-fishing


https://github.com/kermitt2/entity-fishing/blob/master/doc/evaluation.rst
Create one file per document in `entity-fishing/data/corpus/corpus-long/<corpus-name>/RawText/`, with name `<document-title>.<lang>.txt` where lang is the 2 letter abbreviation de/fr/it/en/other.

From `entity-fishing` directory:
```./gradlew annotatedDataGeneration -Pcorpus=dhs-training-de```


# Import pre-annotated data in inception

file-formats: https://inceptiondev.dhlab.epfl.ch/dev/doc/user-guide.html#sect_formats

To import data in inception, use `UIMA CAS XMI (XML 1.1)` format.

# How to get wikipedia page id

Here is the solution (from maxlath answer to https://stackoverflow.com/questions/43746798/how-to-get-wikipedia-pageid-from-wikidata-id):
1) find wikipedia page title (in any language) using wikidata API: `
https://www.wikidata.org/w/api.php?format=json&action=wbgetentities&ids=Q78|Q3044&props=aliases|sitelinks&languages=en
`
2) find wikipedia pageid from page title: `
https://en.wikipedia.org/w/api.php?action=query&titles=Fribourg&format=json
`

inversely, get title from pageid:
https://en.wikipedia.org/w/api.php?action=query&pageids=180312&format=json


Or federated query to dbpedia (on wikidata interface), only works in english, incoherent results (basel entity Q78 yields basel city and basel-stadt canton wikipedia  pages):
```
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX dbo: <http://dbpedia.org/ontology/>  

SELECT ?wikipedia_id where {
    VALUES (?wikidata_id)  {(wd:Q78)}
    SERVICE <http://dbpedia.org/sparql> {
       ?dbpedia_id owl:sameAs ?wikidata_id .
       ?dbpedia_id dbo:wikiPageID ?wikipedia_id 
    } 
}
```
## Wikipedia/wikidata api doc

https://www.mediawiki.org/wiki/API:Main_page


# Entity-fishing/grobid-ner tagset

27 classes: https://grobid-ner.readthedocs.io/en/latest/class-and-senses/


# Evaluation with entity-fishing

To evaluate run: `./gradlew evaluation -Pcorpus=dhs-training-fr`

Note: the actual code for evaluation is in `entity-fishing/src/main/java/com/scienceminer/nerd/evaluation/NEDCorpusEvaluation.java`. You first need to hard-code your corpus name in the `corpora` variable there.