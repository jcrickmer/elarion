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

def delete_link(link_id):
    req(f'/rest/api/3/issueLink/{link_id}', method='DELETE')

def add_blocks(blocker, blocked):
    # Jira API semantics here produce inverse in outward/inward display;
    # this payload has been verified to result in blocker -> blocked.
    payload={
        'type': {'name': 'Blocks'},
        'outwardIssue': {'key': blocked},
        'inwardIssue': {'key': blocker},
    }
    req('/rest/api/3/issueLink', method='POST', payload=payload)

pair_scope={
    'DEV-47','DEV-48','DEV-49','DEV-50','DEV-51','DEV-52','DEV-53','DEV-54','DEV-55','DEV-56','DEV-57',
    'DEV-13','DEV-16','DEV-36','DEV-37','DEV-43','DEV-45'
}

# Remove existing block links inside our scope to prevent cycles/contradictions.
for key in list(pair_scope):
    issue=req(f'/rest/api/3/issue/{key}?fields=issuelinks')
    for l in issue['fields'].get('issuelinks',[]):
        t=l.get('type',{})
        if t.get('name')!='Blocks':
            continue
        other=None
        if 'outwardIssue' in l:
            other=l['outwardIssue']['key']
        if 'inwardIssue' in l:
            other=l['inwardIssue']['key']
        if other in pair_scope:
            delete_link(l['id'])

# Recreate desired dependency order.
ordered=[
    ('DEV-13','DEV-47'),
    ('DEV-47','DEV-48'),
    ('DEV-48','DEV-49'),
    ('DEV-49','DEV-50'),
    ('DEV-50','DEV-51'),
    ('DEV-51','DEV-52'),
    ('DEV-36','DEV-52'),
    ('DEV-52','DEV-53'),
    ('DEV-53','DEV-54'),
    ('DEV-54','DEV-55'),
    ('DEV-37','DEV-55'),
    ('DEV-55','DEV-56'),
    ('DEV-43','DEV-56'),
    ('DEV-56','DEV-57'),
    ('DEV-45','DEV-57'),
    ('DEV-49','DEV-16'),
]
for blocker, blocked in ordered:
    add_blocks(blocker, blocked)

print('updated_links', len(ordered))
