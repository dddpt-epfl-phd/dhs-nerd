# %%
from random import sample, seed
import re

import pandas as pd

from dhs_scraper import DhsArticle


initial_regex = re.compile(r" ([A-Z])\.\W")
 # %%


min_title_element_length = 2
def get_title_initials(title):
    initials = set(s[0] for s in title.split(" ") if len(s)>=min_title_element_length)
    if len(initials)>0:
        return initials
    else:
        return set(s[0] for s in title.split(" "))

# %%

def get_article_identifying_initial(article):
    """Returns the letter being the identifying initial of the article, None if None present
    
    Initials in the texts are first identified as string of the form " X.", where X is any capital letter

    There are 4 cases:
    - 0: return None
    - 1 initial in text which isn't in title initials: return None
    - 1 initial in text which is in title (>90% of articles)
    - more than one initial in the text, and only the most present in
      the text corresponds to a word in the article title -> use this one
    - more than one initial in the text, and only the second most present is 
      in the title: the most present one is an artifact, use the second most present one
    - more than one initial in the text, and the two most present correspond
      to a word in the title. Those are people: the correct initial is the 
      last name one, the one corresponding to the last word in the title.
    """
    text_initials = pd.Series(initial_regex.findall(article.text)).value_counts()

    if len(text_initials)==0:
        return None

    title_initials = [s[0] for s in article.title.split(" ") if s[0].isupper()]
    if len(text_initials)==1:
        if text_initials.index[0] in title_initials:
            return text_initials.index[0]
        else:
            return None
    elif len(text_initials)>1:
        most_present_in_title = text_initials.index[0]
        is_most_present_in_title = most_present_in_title in title_initials
        second_most_present_in_title = text_initials.index[1]
        is_second_most_present_in_title = second_most_present_in_title in title_initials
        if is_most_present_in_title and (not is_second_most_present_in_title):
            return most_present_in_title
        elif (not is_most_present_in_title) and is_second_most_present_in_title:
            return second_most_present_in_title
        elif (not is_most_present_in_title) and (not is_second_most_present_in_title):
            return None
        elif is_most_present_in_title and is_second_most_present_in_title:
            # pick one that is last in title
            chosen = None
            for i in title_initials:
                if i==most_present_in_title:
                    chosen = most_present_in_title
                if i==second_most_present_in_title:
                    chosen = second_most_present_in_title
            return chosen
        else:
            raise Exception(f"get_article_identifying_initial(): UNCOVERED EDGE CASE FOR MORE THAN ONE INITIAL IN TEXT, article:\n{article.title}\n{article.url}\n{article.language}\n{article.id}\n{article.version}")
    else:
        raise Exception(f"get_article_identifying_initial(): UNCOVERED EDGE CASE, article:\n{article.title}\n{article.url}\n{article.language}\n{article.id}\n{article.version}")


