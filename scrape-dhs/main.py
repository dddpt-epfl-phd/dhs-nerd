

from dhs_scraper import DhsArticle

# %%

buffer_size = 100
buffer = [None]*100

# scrape args
max_nb_articles_per_letter = None
parse_articles = True
language="de"
skip_duplicates=True

with open(f"dhs_all_articles_{language}.json", "a") as dhs_all_json_file:
    for i, a in enumerate(DhsArticle.scrape_all_articles(
        language=language,
        max_nb_articles_per_letter=max_nb_articles_per_letter,
        parse_articles = parse_articles,
        force_language = language,
        skip_duplicates = skip_duplicates)):
        if i!=0 and i%buffer_size==0:
            print(f"BUFFER OUT i: {i} \nbuffer[0]:{buffer[0]}\nbuffer[99]:{buffer[99]}")
            dhs_all_json_file.write("\n".join(buffer)+"\n")
        print(f"article {a.name}, i: {i}")
        buffer[i%buffer_size]= a.to_json(ensure_ascii=False)
    print(f"FINAL BUFFER OUT final i: {i}, i%buffer_size: {i%buffer_size} \nbuffer[0]:{buffer[0]}\nbuffer[{i%buffer_size}]:{buffer[i%buffer_size]}")
    dhs_all_json_file.write(",\n".join(buffer[0:((i%buffer_size)+1)])+",\n")



# %%

