import argparse
import base64
import json
import os
import urllib.request

BASE = os.environ.get("JIRA_BASE_URL", "https://jcrickmer.atlassian.net")
EMAIL = os.environ.get("JIRA_EMAIL", "jcrickmer@icloud.com")
TOKEN = os.environ["JIRA_API_TOKEN"]

AUTH = "Basic " + base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()
HEADERS = {
    "Authorization": AUTH,
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def req(path, method="GET", payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(BASE + path, data=data, headers=HEADERS, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode()
        return json.loads(body) if body else {}


def adf_paragraphs(text):
    lines = [line for line in text.splitlines() if line.strip()]
    return {
        "version": 1,
        "type": "doc",
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": line}]}
            for line in lines
        ],
    }


def transition_issue(issue_key, target_status):
    transitions = req(f"/rest/api/3/issue/{issue_key}/transitions").get("transitions", [])
    match = next(
        (t for t in transitions if t.get("to", {}).get("name", "").lower() == target_status.lower()),
        None,
    )
    if not match:
        names = ", ".join(t.get("to", {}).get("name", "") for t in transitions)
        raise RuntimeError(f"Transition '{target_status}' not available for {issue_key}. Available: {names}")

    req(
        f"/rest/api/3/issue/{issue_key}/transitions",
        method="POST",
        payload={"transition": {"id": match["id"]}},
    )


def add_comment(issue_key, comment):
    req(
        f"/rest/api/3/issue/{issue_key}/comment",
        method="POST",
        payload={"body": adf_paragraphs(comment)},
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transition Jira issue and optionally add comment")
    parser.add_argument("issue_key")
    parser.add_argument("target_status")
    parser.add_argument("--comment", default="")
    args = parser.parse_args()

    transition_issue(args.issue_key, args.target_status)
    if args.comment.strip():
        add_comment(args.issue_key, args.comment)

    print(f"updated {args.issue_key} -> {args.target_status}")
