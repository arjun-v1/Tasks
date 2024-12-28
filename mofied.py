import streamlit as st
import requests
from bs4 import BeautifulSoup

def write_to_file(content):
    # print(dir(content))
    of = open('college.html', "w")
    of.write(str(content.tagStack))
    of.close()

    of = open('college_info.html', "w")
    target_attrs = {"class": "table-row"}
    college_items = content.find_all("tr", attrs=target_attrs)
    of.write(get_soup_item_info(college_items))
    of.close()

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"}
    response = requests.get(url, headers=headers)
    print(dir(response))
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def get_soup_item_info(items):
    content = ''
    for item in items:
        try:
            content = content + '\n'.join([str(child)+'\n'for child in item.children])
        except AttributeError as e:
            print(e)
            content = content + str(item)
    return content

def get_colleges_new(soup):
    row_attrs = {"class": "table-row"}
    college_rows = soup.find_all("tr", attrs=row_attrs)
    college_info = []
    for row in college_rows:
        columns = row.find_all('td')
        cd_rank = columns[0].string
        name = columns[1].a.get_attribute_list('data-csm-title')
        location = "".join([s for s in columns[1].find('span', attrs={"class": "location"}).strings])
        
        fees_type = columns[2].find('span', attrs={"class": "short-form"}).get_attribute_list('title')[0]
        fees_value = "".join([s for s in columns[2].find('span', attrs={"class": "text-green"}).strings])
        fees_info = {f"{fees_type}": f"{fees_value}"}

        package_info = []
        package_values = columns[3].findAll('span', attrs={"class": "text-green"})
        package_labels = columns[3].findAll('span', attrs={"class": "text-sm"})
        for label, value in zip(package_labels, package_values):
            label_value = f"{label.string}"
            package_value = "".join([s for s in value.strings])
            package_info.append({label_value: package_value})
        
        college_info.append({'cd_rank': cd_rank,
                             'name': name,
                             'location': location,
                             'fees_info': fees_info,
                             'package_info': package_info})
    return college_info

import pprint
url = "https://collegedunia.com/india-colleges"
soup = get_soup(url)
pprint.pprint(get_colleges_new(soup))
