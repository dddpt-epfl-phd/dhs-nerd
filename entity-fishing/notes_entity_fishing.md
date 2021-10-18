
# Pre-annotate data with entity-fishing


https://github.com/kermitt2/entity-fishing/blob/master/doc/evaluation.rst
Create one file per document in `entity-fishing/data/corpus/corpus-long/<corpus-name>/RawText/`, with name `<document-title>.<lang>.txt` where lang is the 2 letter abbreviation de/fr/it/en/other.

From `entity-fishing` directory:
```./gradlew annotatedDataGeneration -Pcorpus=dhs-training-de```

Import data to inception: use `UIMA CAS XMI (XML 1.1)` format:


# Import pre-annotated data in inception

file-formats: https://inceptiondev.dhlab.epfl.ch/dev/doc/user-guide.html#sect_formats


# How to get wikipedia page id

With page title, asking wikipedia: https://stackoverflow.com/questions/43746798/how-to-get-wikipedia-pageid-from-wikidata-id
you need page title, and adress it to the wikipedia in desired language:
https://en.wikipedia.org/w/api.php?action=query&titles=Fribourg&format=json
inversely, get title from pageid:
https://en.wikipedia.org/w/api.php?action=query&pageids=6235099&format=json


Or federated query to dbpedia (on wikidata interface):
```
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX dbo: <http://dbpedia.org/ontology/>  

SELECT ?wikipedia_id where {
    VALUES (?wikidata_id)  {(wd:Q36378)}
    SERVICE <http://dbpedia.org/sparql> {
       ?dbpedia_id owl:sameAs ?wikidata_id .
       ?dbpedia_id dbo:wikiPageID ?wikipedia_id 
    } 
}
```


# Entity-fishing/grobid-ner tagset

27 classes: https://grobid-ner.readthedocs.io/en/latest/class-and-senses/