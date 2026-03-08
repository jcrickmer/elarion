import base64
import json
import os
import urllib.request

BASE = os.environ.get("JIRA_BASE_URL", "https://jcrickmer.atlassian.net")
EMAIL = os.environ.get("JIRA_EMAIL", "jcrickmer@icloud.com")
TOKEN = os.environ.get("JIRA_API_TOKEN")

auth = "Basic " + base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()
HEADERS = {"Authorization": auth, "Accept": "application/json", "Content-Type": "application/json"}


def req(path, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    r = urllib.request.Request(BASE + path, data=data, headers=HEADERS, method=method)
    with urllib.request.urlopen(r, timeout=30) as resp:
        body = resp.read().decode()
        return json.loads(body) if body else {}

payload = {
    "jql": 'project = DEV AND status = "To Do" ORDER BY priority DESC, created ASC',
    "maxResults": 200,
    "fields": ["summary", "status", "issuetype", "parent", "priority", "labels", "issuelinks"],
}

result = req("/rest/api/3/search/jql", method="POST", payload=payload)
issues = result.get("issues", [])
print(json.dumps({"count": len(issues), "issues": issues}, indent=2))
