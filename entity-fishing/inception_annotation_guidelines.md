

Grobid-NER has 27 classes:
- ACRONYM 
- ANIMAL 
- ARTIFACT 
- AWARD 
- BUSINESS 
- CONCEPT 
- CONCEPTUAL 
- CREATION 
- EVENT 
- IDENTIFIER 
- INSTALLATION 
- INSTITUTION 
- LEGAL 
- LOCATION 
- MEASURE 
- MEDIA 
- NATIONAL 
- ORGANISATION 
- PERIOD 
- PERSON 
- PERSON_TYPE 
- PLANT 
- SPORT_TEAM 
- SUBSTANCE 
- TITLE 
- UNKNOWN 
- WEBSITE 
Extra classes:
- FAMILY
- OCCUPATION

Classes we absolutely need:
- BUSINESS
- EVENT
- INSTITUTION
- MEDIA
- LOCATION
- ORGANISATION
- PERSON

Classes that are relevant but nut primordial:
- INSTALLATION, such as "château de chillon"
- LEGAL, important international treaties/declaration, such as "Traité de Lausanne"
- TITLE, seulement ceux qui sont précisé comme "prince-évêque de Bâle" (et pas juste "prince-évêque" ou conseiller national)
- FAMILY, when not already nested in a person entity

Nice to have classes:
- CONCEPT, such as "feminism", "mythes fondateurs", as there are some concept in DHS, but maybe better not
- NATIONAL? maybe not

Proposition:
For the tags, do the absolutely needed classes and the relevant ones, not the nice-to-have ones.
Regarding the linking, if possible always link to an entity with a link to the DHS. Notably if nested entities, focus on the nested-in-the-dhs one if needed.