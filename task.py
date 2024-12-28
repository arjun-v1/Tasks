import streamlit as st
import requests
from bs4 import BeautifulSoup

'''def write_to_file(content):
    # print(dir(content))
    of = open('college.html', "w")
    of.write(str(content.tagStack))
    of.close()

    of = open('college_info.html', "w")
    target_attrs = {"class": "table-row"}
    college_items = content.find_all("tr", attrs=target_attrs)
    of.write(get_soup_item_info(college_items))
    of.close()'''


def get_colleges(per_page):
    url = "https://collegedunia.com/india-colleges"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #write_to_file(soup)
    
    # Extracting Colleges
    target_attrs = {"class": "clg-logo"}
    college_name_items = soup.find_all("a", attrs=target_attrs)

    college = []

    for name in college_name_items:
        college.append(name.get_attribute_list("data-csm-title")[0])

    # Extracting Locations
    target_attrs = {"class": "location"}
    location_items = soup.find_all("span", attrs=target_attrs)
    location = []

    for i in location_items:
        location.append(i.text.strip())

    # Extracting Fees
    target_attrs = {"class": "text-base"}
    fees_items = soup.find_all("span", attrs=target_attrs)
    fee = []

    for i in fees_items:
     fee.append(i.text.strip())

    # Extracting Courses
    course = []
    target_attrs = {"class": "col-fees"}
    # get all td having "class" value is "col-fees
    course_items = soup.find_all("td", attrs=target_attrs)

    for item in course_items:
        # item is nothing but td
        # get all span inside td having "class value short form"
        val = item.find("span", {"class": "short-form"})
        course.append(val.text.strip())

    # Extracting packages
    target_attrs = {"class": "col-placement"}
    items = soup.find_all("td", attrs=target_attrs)
    packages = []

#select * from soup where tag='td' and class='col-placement';

    for row in items:
        package_info = row.find("span", {"class": "text-green"})
        value = package_info.text.strip()
        package = value and value or None
        packages.append(value)
        
    colleges_info = [{'Name': college[i], 
                      'Location': location[i],
                      'Annual_Fees': fee[i],
                      'Course_Offered': course[i],
                      'Average Package': packages[i]
                     }
                      for i in range(per_page)]
                    
    return colleges_info

'''def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"}
    response = requests.get(url, headers=headers)
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
    for row in college_rows[:1]:
        columns = row.find_all('td')
        cd_rank = columns[0].string
        name = columns[1].a.get_attribute_list('data-csm-title')
        location = "".join([s for s in columns[1].find('span', attrs={"class": "location"}).strings])
        fees_type = columns[2].find('span', attrs={"class": "short-form"}).get_attribute_list('title')[0]
        fees_value = "".join([s for s in columns[2].find('span', attrs={"class": "text-green"}).strings])
        fees_info = {f"{fees_type}": f"{fees_value}"}

        packages = columns[3].findAll('span', attrs={"class": "text-green"})
        package_info = []
        # [(f"{s.next.string}", f"{s}") for package in packages for s in package.strings]
        for p1, p2 in zip(packages[::2], packages[1::2]):
            # package_label, package_value = "", ""
            # for s1, s2 in zip(p1.strings, p2.strings):
            #     label1, value1 = f"{s1.next.string}", f"{s1}"
            #     label2, value2 = f"{s2.next.string}", f"{s2}"
            #     package_label = label1 + label2
            #     package_value = value1 + value2
            #     package_info.append({package_label: package_value})

            A, B = "", ""
            for s1 in p1.strings:
                a, b = f"{s1.next.string}", f"{s1}"
                A = A + a
                B = B + b

            C, D = "", ""
            for s2 in p2.strings:
                c, d = f"{s2.next.string}", f"{s2}"
                C = C + c
                D = D + d
            package_info.extend([{C: B}, {A: D}])
                
        college_info.append({'cd_rank': cd_rank,
                             'name': name,
                             'location': location,
                             'fees_info': fees_info,
                             'package_info': package_info})

    return college_info


    """
    college_attrs = {"class": "col-colleges"}
    college_col_info = item.find_all('td', college_attrs)
    college_info = college_col_info.find_all('span')
    print(get_soup_item_info(college_info))

    course_fees_attrs = {"class": "col-fees"}
    fees_col_info = item.find('td', course_fees_attrs)
    fees_info = fees_col_info.find_all('td')
    print(get_soup_item_info(fees_info))
    
    course_placement_attrs = {"class": "col-placement"}
    placement_col_info = item.find('td', course_placement_attrs)
    placement_info = placement_col_info.find_all('td')
    print(get_soup_item_info(placement_info))
    """
'''
import pprint
no_of_colleges_per_page = 31
url = "https://collegedunia.com/india-colleges"
output = get_colleges(no_of_colleges_per_page)
pprint.pprint(output)

#soup = get_soup(url)
#pprint.pprint(get_colleges_new(soup))

# st.title('College Information App')

# if st.button('Get colleges'):
#     st.write('Fetching data...')
#     colleges = get_colleges()
#     print(colleges)
#     for college in colleges:
#         st.write(f"Name: {college['name']}")
#         st.write(f"Location: {college['location']}")
#         st.write(f"Courses Offered: {college['courses']}")
#         st.write(f"Fees: {college['fees']}")
#         st.write(f"Ranking: {college['ranking']}")
