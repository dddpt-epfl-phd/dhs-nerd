from os import path

"""
This file centralizes paths to data files/folders for the whole project.
Paths are always relative to three folders down from root (-> scripts are run in their respective ./scripts/<step>/ folder)
"""

# scripts are always assumed to be two directories down from root
ROOT_FOLDER = "../../.."

DATA_FOLDER = path.join(ROOT_FOLDER, "data")
REPORTS_FOLDER = path.join(ROOT_FOLDER, "reports")

FIGURES_FOLDER = path.join(REPORTS_FOLDER, "figures")


# website
#####################

WEB_FOLDER= path.join(ROOT_FOLDER, "web")

S5_WEBSITE_DATA_FOLDER = path.join(DATA_FOLDER, "website")

website_hds_thematic_indexation = path.join(WEB_FOLDER, "hds_thematic_indexation")

S5_WEBSITE_SINGLE_ARTICLES_FOLDER = path.join(S5_WEBSITE_DATA_FOLDER, "single-dhs-articles")
S5_WEBSITE_SINGLE_ARTICLES_LOCALIZED_FOLDER = path.join(S5_WEBSITE_SINGLE_ARTICLES_FOLDER, "<LANGUAGE>")

# s0_scrape_dhs
#####################



S0_DATA_FOLDER = path.join(DATA_FOLDER, "scrape_dhs")

# s0_scrape_dhs/s0_scrape.py
S0_JSONL_ALL_ARTICLES_FILE = path.join(S0_DATA_FOLDER, "dhs_<LANGUAGE>_all_articles_content.jsonl")
S0_JSONL_ALL_ARTICLES_PARSED_FILE = path.join(S0_DATA_FOLDER, "dhs_<LANGUAGE>_all_articles_parsed.jsonl")
S0_JSONL_ALL_ARTICLES_NO_PAGE_FILE = path.join(S0_DATA_FOLDER, "no-page-content","dhs_<LANGUAGE>_all_articles_content.jsonl")

S0_THEMES_CATEGORY = "themes"
S0_PEOPLE_CATEGORY = "people"
S0_FAMILIES_CATEGORY = "families"
S0_SPATIAL_CATEGORY = "spatial"
S0_DHS_CATEGORIES = [S0_THEMES_CATEGORY, S0_PEOPLE_CATEGORY, S0_FAMILIES_CATEGORY, S0_SPATIAL_CATEGORY]

S0_JSONL_ARTICLES_BY_CATEGORIES_FILES = {
    category: path.join(S0_DATA_FOLDER, f"dhs_<LANGUAGE>_category_{category}_articles.jsonl")
    for category in S0_DHS_CATEGORIES
}

# s0 s0_scrape_dhs/s1_dhs_stats.py
s0_png_articles_lengths_by_category_figure = path.join(FIGURES_FOLDER, "s0_articles_lengths_by_category.png")
s0_png_percent_articles_in_wd_by_category = path.join(FIGURES_FOLDER, "s0_percent_articles_in_wd_by_category.png")


# s1 s1_wikidata_dhs_linking
#####################

S1_DATA_FOLDER = path.join(DATA_FOLDER, "wikidata_dhs_linking")

S1_WIKIDATA_DHS_WIKIPEDIA_LINKS = path.join(S1_DATA_FOLDER, "wikidata_dhs_wikipedia_articles_gndid_instanceof.csv")
S1_WIKIDATA_DE_LABELS = path.join(S1_DATA_FOLDER, "wikidata_de_labels.csv")

# s1 s2_entity_fishing evaluation
#####################
S2_INCEPTION_DATA_FOLDER = path.join(DATA_FOLDER, "inception")
S2_ENTITY_FISHING_DATA_FOLDER = path.join(DATA_FOLDER, "entity-fishing")
S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER = path.join(DATA_FOLDER, "entity-fishing-evaluation")

S2_INCEPTION_SAMPLED_ARTICLES_IDS = path.join(S2_INCEPTION_DATA_FOLDER, "sampled_articles_ids.json")
S2_INCEPTION_SAMPLED_ARTICLES = path.join(S2_INCEPTION_DATA_FOLDER, "sampled_articles_<LANGUAGE>.jsonl")

S2_ENTITY_FISHING_CORPUS_FOLDER = path.join(ROOT_FOLDER, f"entity-fishing/entity-fishing/data/corpus/corpus-long/dhs-training-<LANGUAGE>/")
S2_ENTITY_FISHING_ANNOTATION_OUTPUT_FILE = path.join(S2_ENTITY_FISHING_CORPUS_FOLDER,f"dhs-training-<LANGUAGE>.xml")
S2_ENTITY_FISHING_CORPUS_RAWTEXT_FOLDER = path.join(S2_ENTITY_FISHING_CORPUS_FOLDER, "RawText/")

S2_INCEPTION_IMPORT_FOLDER = path.join(S2_INCEPTION_DATA_FOLDER, "inception-import-xml/")
S2_INCEPTION_ANNOTATIONS_2_11_FOLDER = path.join(S2_INCEPTION_DATA_FOLDER, 'inception-annotation-2-11')
S2_ENTITY_FISHING_2_11_PREDICTION_CORPUS_FOLDER = path.join(S2_ENTITY_FISHING_DATA_FOLDER, 'dhs-training-<LANGUAGE>-2-11/')
S2_ENTITY_FISHING_2_11_PREDICTION_OUTPUT_FILE = path.join(S2_ENTITY_FISHING_2_11_PREDICTION_CORPUS_FOLDER,f"dhs-training-<LANGUAGE>.xml")
S2_ENTITY_FISHING_2_11_RAWTEXT_FOLDER = path.join(S2_ENTITY_FISHING_2_11_PREDICTION_CORPUS_FOLDER, "RawText/")
S2_INCEPTION_ANNOTATIONS_16_12_FOLDER = path.join(S2_INCEPTION_DATA_FOLDER, 'inception-annotation-16-12')
S2_INCEPTION_USER_NAME = "dddpt"

S2_ENTITY_FISHING_2_11_OWN_EVALUATION_TRUE_FILE = path.join(S2_INCEPTION_ANNOTATIONS_2_11_FOLDER,"dhs-<LANGUAGE>-true-entity-fishing-scorer.xml")

# folder to re-import annotated 2-11 documents in inception after their text has been re-adapted to the new DhsArticles text content
S2_INCEPTION_REIMPORT_2_11_FOLDER = path.join(S2_INCEPTION_DATA_FOLDER, "inception-re-import-xmi-2-11/")


S2_CLEF_HIPE_FILE_SUFFIX = "-clef-hipe-scorer-conllu.tsv"
S2_CLEF_HIPE_PRED_FILE_2_11 = path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,f"dhs-2-11-<LANGUAGE>-pred"+S2_CLEF_HIPE_FILE_SUFFIX)
S2_CLEF_HIPE_TRUE_FILE_2_11 = path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,f"dhs-2-11-<LANGUAGE>-true"+S2_CLEF_HIPE_FILE_SUFFIX)
S2_CLEF_HIPE_PRED_FILE_16_12 = path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,f"dhs-16-12-<LANGUAGE>-pred"+S2_CLEF_HIPE_FILE_SUFFIX)
S2_CLEF_HIPE_TRUE_FILE_16_12 = path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,f"dhs-16-12-<LANGUAGE>-true"+S2_CLEF_HIPE_FILE_SUFFIX)
S2_CLEF_HIPE_TAGGED_FILE = path.join(S2_ENTITY_FISHING_EVALUATION_DATA_FOLDER,f"dhs-<TAG>-<LANGUAGE>-<PREDTRUE>"+S2_CLEF_HIPE_FILE_SUFFIX)


# s1 s4 entity_fishing-linking:
#####################

S4_ENTITY_FISHING_LINKING_DATA_FOLDER = path.join(DATA_FOLDER, "entity-fishing-linking")

S4_ENTITY_FISHING_LINKING_TEST_DATA_FOLDER = path.join(S4_ENTITY_FISHING_LINKING_DATA_FOLDER, "test")
S4_JSONL_ENTITY_FISHING_LINKING_TEST_LINKED_DHSA = path.join(S4_ENTITY_FISHING_LINKING_TEST_DATA_FOLDER, "linked-dhs-<LANGUAGE>-test.jsonl")


S4_JSONL_ALL_ARTICLES_LINKED_FILE = path.join(S4_ENTITY_FISHING_LINKING_DATA_FOLDER, "dhs_<LANGUAGE>_all_articles_linked.jsonl")
S4_ENTITY_FISHING_TIMED_OUT_ARTICLES_FILE = path.join(S4_ENTITY_FISHING_LINKING_DATA_FOLDER, "dhs_<LANGUAGE>_timed_out_articles.txt")

s4_nb_articles_per_year_figure = path.join(FIGURES_FOLDER, "s4_nb_articles_per_year.png")
s4_avg_nb_links_per_article_per_year_figure = path.join(FIGURES_FOLDER, "s4_avg_nb_links_per_article_per_year.png")
s4_nb_links_per_1000char_per_year_figure = path.join(FIGURES_FOLDER, "s4_avg_nb_links_per_1000char_per_year.png")
s4_nb_hds_ef_links_per_1000char_per_year_figure = path.join(FIGURES_FOLDER, "s4_nb_hds_ef_links_per_1000char_per_year.png")
s4_hds_ef_links_per_article_distribution_figure = path.join(FIGURES_FOLDER, "s4_hds_ef_links_per_article_distribution.png")
s4_hds_ef_links_per_article_distribution_breakdown_figure = path.join(FIGURES_FOLDER, "s4_hds_ef_links_per_article_distribution_breakdown.png")
s4_nb_links_from_hds_and_ef_figure = path.join(FIGURES_FOLDER, "s4_nb_links_from_hds_and_ef.png")
s4_hds_ef_nb_linking_to_article_distribution_breakdown_figure = path.join(FIGURES_FOLDER, "s4_nb_linking_to_article_distribution_breakdown.png")
s4_hds_ef_nb_linking_to_article_distribution_by_category_breakdown_figure = path.join(FIGURES_FOLDER, "s4_hds_ef_nb_linking_to_article_distribution_by_category_breakdown.png")
s4_hds_ef_links_to_categories_distribution = path.join(FIGURES_FOLDER, "s4_hds_ef_links_to_categories_distribution.png")


# s2 s0_spatial_articles
#####################

s2_hds_thematic_indexation_folder = path.join(DATA_FOLDER, "hds_thematic_indexation")

tag_tree_with_ids_filename = "tag_tree_with_ids_<CASE>.json"
s2_s0_tag_tree_with_ids = path.join(s2_hds_thematic_indexation_folder,tag_tree_with_ids_filename)
s2_s0_tag_tree_with_ids_web = path.join(website_hds_thematic_indexation,tag_tree_with_ids_filename)

s2_polities_to_extract_folder = path.join(DATA_FOLDER, "polities_to_extract")
s2_s1_polities_tags_extraction_rules = path.join(s2_polities_to_extract_folder,"polities_tags_extraction_rules.csv")
s2_s1_polities_tags_extraction_rules_hand_filled = path.join(s2_polities_to_extract_folder,"polities_tags_extraction_rules_hand_filled.csv")


s2_hds_article_titles_terms_csv = path.join(s2_polities_to_extract_folder,"hds_article_titles_terms.csv")
s2_hds_article_titles_terms_to_remove_csv = path.join(s2_polities_to_extract_folder,"hds_article_titles_terms_to_remove.csv")
s2_hds_article_titles_terms_to_remove_hand_corrected_csv = path.join(s2_polities_to_extract_folder,"hds_article_titles_terms_to_remove_HAND_CORRECTED.csv")
s2_hds_article_titles_statuswords_csv = path.join(s2_polities_to_extract_folder,"hds_article_titles_statuswords.csv")
s2_hds_article_titles_statuswords_hand_corrected_csv = path.join(s2_polities_to_extract_folder,"hds_article_titles_statuswords_HAND_CORRECTED.csv")
s2_hds_article_titles_statuswords_json = path.join(s2_polities_to_extract_folder,"hds_article_titles_statuswords.json")
s2_hds_article_titles_statuswords_hand_corrected_json = path.join(s2_polities_to_extract_folder,"hds_article_titles_statuswords_HAND_CORRECTED.json")
s2_hds_tag_default_status_word = path.join(s2_polities_to_extract_folder, "hds_tag_default_status_word.json")
s2_hds_tagname_to_initial = path.join(s2_polities_to_extract_folder, "tagname_to_initial.json")
s2_hds_title_terms_indicating_extra_polity = path.join(s2_polities_to_extract_folder, "title_terms_indicating_extra_polity.csv")
s2_polities_list_csv = path.join(s2_polities_to_extract_folder,"polities_list.csv")

s2_polities_txt_folder = path.join(s2_polities_to_extract_folder, "polities_txt")

def localize(path, language):
    return path.replace("<LANGUAGE>", language)


