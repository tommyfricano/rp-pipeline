import os
import requests
import random
from requests.auth import HTTPBasicAuth

# Confluence credentials and page information
CONFLUENCE_URL = "https://tjfricano.atlassian.net/wiki/rest/api/content"
CONFLUENCE_PAGE_ID = str(random.randint(100000, 999999))
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")

# Read README.md content
with open("README.md", "r") as file:
    readme_content = file.read()

# Create the payload
payload = {
    "version": {"number": 2},  # You might need to increment this version number
    "title": "Your Page Title",
    "type": "page",
    "body": {
        "storage": {
            "value": f"<pre>{readme_content}</pre>",
            "representation": "storage",
        }
    },
}

# Send the request to update the Confluence page
response = requests.put(
    f"{CONFLUENCE_URL}/{CONFLUENCE_PAGE_ID}",
    json=payload,
    headers={"Content-Type": "application/json",
             "Authorization": f"Basic {CONFLUENCE_API_TOKEN}"},
)

# Check if the upload was successful
if response.status_code == 200:
    print("README.md successfully uploaded to Confluence.")
else:
    print(f"Failed to upload README.md to Confluence: {response.status_code}")
    print(response.text)
