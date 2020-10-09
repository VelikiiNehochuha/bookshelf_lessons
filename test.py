"""
if "a" == "a":
    print("Условие 1 сработало")

if "a" != "a":
    print("Условие 2 не сработало")


def my_function():
    print("Hello world")

my_function()


def my_function_with_args(arg_a, arg_b):
    return arg_a + arg_b

a = my_function_with_args(3, 5)
print(a)
"""
import json

import requests
from bs4 import BeautifulSoup


# with open('test.html', 'wb') as f:
#     f.write(res.text.encode("utf-8"))


name = "Кратчайшая история времени"
author = "Стивен Хокинг"

response = requests.get(f'https://www.litres.ru/pages/rmd_search/?q={name} {author}')
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')
search_results = soup.find(id="searchresults")

first_result = search_results.find("div", {"class": "search__item"})
cover = first_result.find("div", {"class": "cover"})
raw_data = cover.get("data-obj")
raw_params = raw_data.strip('{').strip('}').split(',')
params = {}
for raw_param in raw_params:
    name_value = raw_param.split(':')
    params[name_value[0]] = name_value[1].strip().strip("'")
print(params)
print(params["available"])
print(params["price"])


def check_book(author, name):
    return {
        "availiable": "?",
        "price": "?"
    }





