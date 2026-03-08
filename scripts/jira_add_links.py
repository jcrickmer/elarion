import base64, json, os, urllib.request
BASE=os.environ.get('JIRA_BASE_URL','https://jcrickmer.atlassian.net')
EMAIL=os.environ.get('JIRA_EMAIL','jcrickmer@icloud.com')
TOKEN=os.environ['JIRA_API_TOKEN']
auth='Basic '+base64.b64encode(f'{EMAIL}:{TOKEN}'.encode()).decode()
H={'Authorization':auth,'Accept':'application/json','Content-Type':'application/json'}

def req(path, method='GET', payload=None):
    data=None if payload is None else json.dumps(payload).encode()
    r=urllib.request.Request(BASE+path, data=data, headers=H, method=method)
    with urllib.request.urlopen(r, timeout=30) as resp:
        b=resp.read().decode()
        return json.loads(b) if b else {}

def add_blocks(blocker, blocked):
    payload={'type': {'name':'Blocks'}, 'outwardIssue': {'key': blocked}, 'inwardIssue': {'key': blocker}}
    req('/rest/api/3/issueLink', method='POST', payload=payload)

for blocker, blocked in [
    ('DEV-36','DEV-37'),
    ('DEV-37','DEV-38'),
    ('DEV-37','DEV-40'),
    ('DEV-38','DEV-39'),
]:
    add_blocks(blocker, blocked)

print('added',4)
