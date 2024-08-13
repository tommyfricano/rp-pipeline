import os
import requests
import random
import json
from requests.auth import HTTPBasicAuth

CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_PAGE_ID = os.environ.get("CONFLUENCE_PAGE_ID")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")

with open("README.md", "r") as file:
    readme_content = file.read()


table_html = """
<table>
    <tr>
        <th>Column 1</th>
        <th>Column 2</th>
    </tr>
    <tr>
        <td>Value 1</td>
        <td>Value 2</td>
    </tr>
    <tr>
        <td>Value 3</td>
        <td>Value 4</td>
    </tr>
</table>
"""

# Create the payload with the table and the README content
payload = {
    "version": {"number": 2},
    "title": "{CONFLUENCE_PAGE_TITLE}",
    "type": "page",
    "body": {
        "storage": {
            "value": f"<pre>{readme_content}</pre><br/>{table_html}",
            "representation": "storage",
        }
    },
}
#     payload = {
#         "version": {"number": 2},
#         "title": "{CONFLUENCE_PAGE_TITLE}",
#          "type": "page",
#          "body": {
#             "storage": {
#                 "value": f"<pre>{readme_content}</pre>",
#                 "representation": "storage",
#             }
#          },
#     }
    response = requests.put(
        f"{CONFLUENCE_URL}/{CONFLUENCE_PAGE_ID}",
        json=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Basic {CONFLUENCE_API_TOKEN}"},
    )



if response.status_code >= 300:
    print(f"Failed to upload README.md to Confluence: {response.status_code}")
    print(response.text)
else:
    print("README.md successfully uploaded to Confluence.")

