

# dhs-nerd: Historical Dictionary of Switzerland (HDS) Named Entity Recognition and Disambiguation 

In this work, our aim is to create a cross-linked version of [the Historical Dictionary of Switzerland (HDS)](https://hls-dhs-dss.ch), a trilingual online encyclopedia on the history of Switzerland in French, German and Italian. We carried out and evaluated named entity recognition and linking on the 36’000 articles of the HDS. For named entity recognition and linking we used the entity-fishing tool. Based on the results, we created a demonstration web interface for a cross-linked HDS in the three languages. The cross-linked HDS has an average of 6 HDS links per 1000 characters against 1 HDS link in the current version of the HDS. However, around 60% of entities present in the HDS cannot be linked with our approach as those entities are absent from entity-fishing’s training set, Wikipedia. The cross-linked HDS demonstration interface is available here: https://dddpt-epfl-phd.github.io/dhs-nerd/. It allows for a more enticing exploration experience of the HDS.

The [full report is available here](https://github.com/dddpt-epfl-phd/dhs-nerd/raw/master/reports/HDS%20Named%20Entity%20Linking%20Report.pdf)

## Repo structure

This project is organized as follows:
- `scripts/` contains all the code to download the HDS, link it with entity-fishing and compute statistics and plots. Substeps are:
    + `s0_scrape_dhs/`
    + `s1_wikidata_dhs_linking/`
    + `s2_entity_fishing_evaluation/`
    + `s3_qualitative_errors_display/`
    + `s4_entity_fishing_linking/`
- `src/` contains 4 submodules that are used across the project:
    + `CLEF-HIPE-2020-scorer/`: scorer for NLP tasks.
    + `dhs_scraper/`: small library to scrape HDS articles with metadata.
    + `inception_fishing/`: basic Corpus-Document-annotation data-structures with import/export capability to all the used frameworks (entity-fishing, inception annotation platform).
    + `nlp_pred_true_comparator/`: small library to visually compare NLP prediction results with ground truth.
- `web/` contains the code for the linked HDS web interface.
- `docs/` github pages folder for the linked HDS web interface (not documentation, do not touch).
