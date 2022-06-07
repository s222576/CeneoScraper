from googletrans import Translator
from bs4 import BeautifulSoup
import requests
import json

dest = "en"
src = "pl"
translator = Translator()

def get_element(parent, selector, attribute = None, return_list = False):
    try:
        if return_list:
            return ", ".join([item.text.strip() for item in parent.select(selector)])
        if attribute:
            return parent.select_one(selector)[attribute]
        return parent.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None

def translate(text, src=src, dest=dest):
    try:
        return translator.translate(text, src=src, dest=dest).text
    except (AttributeError, TypeError):
        print("Error")
        return ""

opinion_elements = {
    "author":["span.user-post__author-name"],
    "rcmd": ["span.user-post__author-recomendation > em"],
    "score": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "posted_on": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "bought_on": ["span.user-post__published > time:nth-child(2)", "datetime"],
    "useful_for": ["button.vote-yes > span"],
    "useless_for": ["button.vote-no > span"],
    "pros": ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "cons": ["div.review-feature__title--negatives ~ div.review-feature__item", None, True]
}

product_id = input("Please enter the product id: ")
url = f"https://www.ceneo.pl/{product_id}#tab=reviews"

all_opinions = []

while (url):
    print(url)
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")

    for opinion in opinions:
        single_opinion = {
            key: get_element(opinion, *values)
            for key, values in opinion_elements.items() 
        }
        single_opinion["opinion_id"] = opinion["data-entry-id"]
        single_opinion["rcmd"] = True if single_opinion["rcmd"] == "Polecam" else False if single_opinion["rcmd"] == "Nie polecam" else None
        single_opinion["score"] = float(single_opinion["score"].split("/")[0].replace(",", "."))
        single_opinion["useful_for"] = int(single_opinion["useful_for"])
        single_opinion["useless_for"] = int(single_opinion["useless_for"])
        single_opinion["content_en"] = translate(single_opinion["content"]) if single_opinion["content"] else ""
        single_opinion['pros_en'] = translate(single_opinion['pros']) if single_opinion["pros"] else ""
        single_opinion['cons_en'] = translate(single_opinion['cons']) if single_opinion["cons"] else ""
        all_opinions.append(single_opinion)

    try:
        url = "https://www.ceneo.pl"+get_element(page_dom,"a.pagination__next","href")
    except TypeError: 
        url = None

with open(f"opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii=False)