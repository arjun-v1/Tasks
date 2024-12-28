import json
import requests
import sys

import streamlit as st


def get_url():
    urls = [
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjAsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ==",
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjEsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ==",
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjIsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ==",
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjMsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ==",
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjQsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ==",
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjUsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ==",
        "https://collegedunia.com/web-api/listing?data=eyJ1cmwiOiJpbmRpYS1jb2xsZWdlcyIsInBhZ2UiOjYsInZpZXciOiJ0YWJsZSIsImhhc190ZXh0X3JhbmtpbmciOmZhbHNlfQ=="
    ]
    return urls


def get_colleges():
  
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36"}

    for url in get_url():
        print(f"URL: {url}")
        response = requests.get(url, headers=headers)
        content = json.loads(response.content)
        colleges = content['colleges']
   
        for college in colleges:
            yield {
                    'State Id': college['state_id'],
                    'College Name': college['college_name'],
                    'State': college['state'],
                    'Approvals': college['approvals'],
                    'Fees': college['fees'],
                    'Placement': college['placement']
                }


st.title('College Information App')
if st.button('Get colleges'):
    no_colleges = int(sys.argv[1])
    for i, college in enumerate(get_colleges()):
        st.write(f"{i+1}", college)
        if i+1 == no_colleges:
            break

