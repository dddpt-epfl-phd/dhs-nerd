# Generating the data

- `s0_sample_dhs_training_data_for_entity_fishing.py`: Generates a sample of 10 DHS articles in FR and DE for entity-fishing
- `s1_from_entity_fishing_to_inception.py`: Prepares the output from entity-fishing for annotation in inception (also creates CLEF-HIPE SCORER pred .tsv file)
- `s2_from_inception_annotation_to_entity_fishing.py`: Takes the output of inception (UIMA CAS XMI 1.1 format) and transforms it back to a format readable by entity-fishing as well as the CLEF-HIPE 2020 scorer
- `s3_scoring_only_dhs_entities.py`: Creates CLEF-HIPE scorer tsv files containing only entities that are in the dhs and wikidata OR in the dhs and the wikipedia of the corresponding language
- `s4_pred_true_discrepancy_investigation.py`: Investigates the discrepancies between pred_ and true_

# Scoring:

Using the CLEF-HIPE scorer, run from CLEF-Hipe folder:
`python clef_evaluation.py --ref ../scoring_data/dhs-fr-true-clef-hipe-scorer-conllu.tsv --pred ../scoring_data/dhs-fr-pred-clef-hipe-scorer-conllu.tsv --task nel --outdir ../scoring_data/ --skip-check`

