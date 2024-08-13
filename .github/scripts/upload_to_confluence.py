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
    readme_lines = file.readlines()

table_rows = "".join(f"<tr><td><pre>{line}</pre></td></tr>" for line in readme_lines)

 # Create the full table HTML
table_html = f"""
 <table>
     <tr>
         <th>README Content</th>
     </tr>
     {table_rows}
 </table>
 """

 # Create the payload with the table
payload = {
     "version": {"number": 3},  # Increment this number for each update
     "title": "{CONFLUENCE_PAGE_TITLE}",
     "type": "page",
     "body": {
         "storage": {
             "value": table_html,
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

