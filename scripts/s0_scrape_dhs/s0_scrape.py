# %%


import sys
sys.path.append("../../src")
sys.path.append("../../scripts")

from dhs_scraper import DhsArticle, stream_to_jsonl
from file_paths import S0_JSONL_ALL_ARTICLES_FILE, S0_JSONL_ARTICLES_BY_CATEGORIES_FILES, S0_THEMES_CATEGORY, S0_PEOPLE_CATEGORY, S0_FAMILIES_CATEGORY, S0_SPATIAL_CATEGORY, localize

# %% scrape args

language="de"

buffer_size = 100
max_nb_articles_per_letter = None
parse_articles = True
skip_duplicates=True


# %% Scrape articles content
if True:

    jsonl_articles_content_file = localize(S0_JSONL_ALL_ARTICLES_FILE, language)
    already_visited_ids = set(DhsArticle.get_articles_ids(jsonl_articles_content_file))
    stream_to_jsonl(
        jsonl_articles_content_file,
        DhsArticle.scrape_all_articles(
            language=language,
            max_nb_articles_per_letter=max_nb_articles_per_letter,
            parse_articles = parse_articles,
            force_language = language,
            skip_duplicates = skip_duplicates,
            already_visited_ids = already_visited_ids
        ),
        buffer_size=buffer_size
    )


# %% Scrape by categories (available from top of DHS): themes, people, families, space

if False:
    # themes
    jsonl_themes_articles_file = localize(S0_JSONL_ARTICLES_BY_CATEGORIES_FILES[S0_THEMES_CATEGORY], language)
    already_visited_themes_ids = set(DhsArticle.get_articles_ids(jsonl_themes_articles_file))
    stream_to_jsonl(
        jsonl_themes_articles_file,
        DhsArticle.scrape_articles_from_search_url(
            f"https://hls-dhs-dss.ch/fr/search/category?text=*&sort=score&sortOrder=desc&collapsed=true&r=1&rows=100&f_hls.lexicofacet_string=0%2F016900.&firstIndex=",
            force_language = language,
            skip_duplicates = skip_duplicates,
            already_visited_ids = already_visited_themes_ids,
            rows_per_page=100
        ),
        buffer_size=buffer_size
    )

    # %%

    # people
    jsonl_people_articles_file = localize(S0_JSONL_ARTICLES_BY_CATEGORIES_FILES[S0_PEOPLE_CATEGORY], language)
    already_visited_people_ids = set(DhsArticle.get_articles_ids(jsonl_people_articles_file))
    stream_to_jsonl(
        jsonl_people_articles_file,
        DhsArticle.scrape_articles_from_search_url(
            f"https://hls-dhs-dss.ch/fr/search/category?text=*&sort=score&sortOrder=desc&collapsed=true&r=1&rows=100&f_hls.lexicofacet_string=0%2F000100.&firstIndex=",
            force_language = language,
            skip_duplicates = skip_duplicates,
            already_visited_ids = already_visited_people_ids,
            rows_per_page=100
        ),
        buffer_size=buffer_size
    )
    # %%

    # families
    jsonl_families_articles_file = localize(S0_JSONL_ARTICLES_BY_CATEGORIES_FILES[S0_FAMILIES_CATEGORY], language)
    already_visited_families_ids = set(DhsArticle.get_articles_ids(jsonl_families_articles_file))
    stream_to_jsonl(
        jsonl_families_articles_file,
        DhsArticle.scrape_articles_from_search_url(
            f"https://hls-dhs-dss.ch/fr/search/category?text=*&sort=score&sortOrder=desc&collapsed=true&r=1&rows=100&f_hls.lexicofacet_string=0%2F000200.&firstIndex=",
            force_language = language,
            skip_duplicates = skip_duplicates,
            already_visited_ids = already_visited_families_ids,
            rows_per_page=100
        ),
        buffer_size=buffer_size
    )
    # %%

    # spatial
    jsonl_spatial_articles_file = localize(S0_JSONL_ARTICLES_BY_CATEGORIES_FILES[S0_SPATIAL_CATEGORY], language)
    already_visited_spatial_ids = set(DhsArticle.get_articles_ids(jsonl_spatial_articles_file))
    stream_to_jsonl(
        jsonl_spatial_articles_file,
        DhsArticle.scrape_articles_from_search_url(
            f"https://hls-dhs-dss.ch/fr/search/category?text=*&sort=score&sortOrder=desc&collapsed=true&r=1&rows=100&f_hls.lexicofacet_string=0%2F006800.&firstIndex=",
            force_language = language,
            skip_duplicates = skip_duplicates,
            already_visited_ids = already_visited_spatial_ids,
            rows_per_page=100
        ),
        buffer_size=buffer_size
    )
    # %%
