# %%

import re

from dhs_scraper import DhsArticle


language="de"
output_file = f"dhs_all_articles_{language}.jsonl"


# %%


id_regex = re.compile(r'^.+?"id": "(\d+)"')
with open(output_file, "r") as dhs_all_json_file:
    already_visited_ids = set(id_regex.search(line).group(1) for line in dhs_all_json_file if len(line)>0)

# %%

buffer_size = 100
buffer = [None]*100

# scrape args
max_nb_articles_per_letter = None
parse_articles = True
skip_duplicates=True

with open(output_file, "a") as dhs_all_json_file:
    for i, a in enumerate(DhsArticle.scrape_all_articles(
        language=language,
        max_nb_articles_per_letter=max_nb_articles_per_letter,
        parse_articles = parse_articles,
        force_language = language,
        skip_duplicates = skip_duplicates,
        already_visited_ids = already_visited_ids)):
        if i!=0 and i%buffer_size==0:
            print(f"BUFFER OUT i: {i} \nbuffer[0]:{buffer[0]}\nbuffer[99]:{buffer[99]}")
            dhs_all_json_file.write("\n".join(buffer)+"\n")
        print(f"article {a.name}, i: {i}")
        buffer[i%buffer_size]= a.to_json(ensure_ascii=False)
    print(f"FINAL BUFFER OUT final i: {i}, i%buffer_size: {i%buffer_size} \nbuffer[0]:{buffer[0]}\nbuffer[{i%buffer_size}]:{buffer[i%buffer_size]}")
    dhs_all_json_file.write(",\n".join(buffer[0:((i%buffer_size)+1)])+",\n")



# %%

