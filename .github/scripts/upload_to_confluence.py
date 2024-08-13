import os
import requests
import random
import json
from requests.auth import HTTPBasicAuth

# Confluence credentials and page information
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_PAGE_TITLE = os.environ.get("CONFLUENCE_PAGE_TITLE")
CONFLUENCE_NEW_PAGE_ID = str(random.randint(100000, 999999))
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")

# Read README.md content
with open("README.md", "r") as file:
    readme_content = file.read()

print(readme_content)

get_response = requests.get(
    f"{CONFLUENCE_URL}?title={CONFLUENCE_PAGE_TITLE}",
    headers={"Content-Type": "application/json",
             "Authorization": f"Basic {CONFLUENCE_API_TOKEN}"},
)

print(get_response)

response = ""

if get_response.status_code == 404:
    payload = {
        "version": {"number": 1},
        "title": "{CONFLUENCE_PAGE_TITLE}",
         "type": "page",
         "body": {
            "storage": {
                "value": f"<pre>{readme_content}</pre>",
                "representation": "storage",
            }
         },
    }
    response = requests.post(
        f"{CONFLUENCE_URL}",
        json=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Basic {CONFLUENCE_API_TOKEN}"},
    )
else:
    json_res = json.loads(get_response.text)
    page_id = json_res.get("results", [])[0].get("id")
    print(page_id)
    payload = {
        "version": {"number": 2},
        "title": "{CONFLUENCE_PAGE_TITLE}",
         "type": "page",
         "body": {
            "storage": {
                "value": f"<pre>{readme_content}</pre>",
                "representation": "storage",
            }
         },
    }
    response = requests.put(
        f"{CONFLUENCE_URL}/"+page_id,
        json=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Basic {CONFLUENCE_API_TOKEN}"},
    )

if response.status_code >= 300:
    print(f"Failed to upload README.md to Confluence: {response.status_code}")
    print(response.text)
else:
    print("README.md successfully uploaded to Confluence.")

