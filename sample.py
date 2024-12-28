import streamlit as st
import requests
from bs4 import BeautifulSoup


def get_index_page(url):
    url = "https://docs.python.org/3/library/index.html"
    response = requests.get(url)
    index_page = BeautifulSoup(response.content, 'html.parser')

    return index_page

def get_items(page):
        
    target_attrs = {"class": "pre"}
    items = page.find_all("span", attrs=target_attrs)
    print(f"items: {items}")
    for college in items:
        print(college.string)

def get_build_in_functions(page):
    target_attrs = {"class": "toctree-l1"}
    list_of_li = page.find_all("li", attrs=target_attrs)
    items = list_of_li[1].find_all('li')
    build_ins = [item.string for item in items]
    return build_ins


url = "https://docs.python.org/3/library/index.html"
index_page = get_index_page(url)
#items = get_items(index_page)
build_ins = get_build_in_functions(index_page)
print(build_ins)

