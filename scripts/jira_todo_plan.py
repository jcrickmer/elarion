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

payload={
  'jql':'project = DEV AND status = "To Do" ORDER BY created ASC',
  'maxResults':300,
  'fields':['summary','status','issuetype','parent','priority','issuelinks']
}
issues=req('/rest/api/3/search/jql','POST',payload)['issues']

by_key={i['key']:i for i in issues}

rows=[]
for i in issues:
    f=i['fields']
    key=i['key']
    parent=(f.get('parent') or {}).get('key')
    blocks=[]
    blocked_by=[]
    for l in f.get('issuelinks',[]):
        t=l.get('type',{})
        if 'outwardIssue' in l and t.get('outward')=='blocks':
            blocks.append(l['outwardIssue']['key'])
        if 'inwardIssue' in l and t.get('inward')=='is blocked by':
            blocked_by.append(l['inwardIssue']['key'])
    rows.append({
      'key':key,
      'type':f['issuetype']['name'],
      'summary':f['summary'],
      'parent':parent,
      'blocked_by':blocked_by,
      'blocks':blocks,
      'priority':(f.get('priority') or {}).get('name')
    })

# categorize
cats={'foundation':[],'auth_ui':[],'db':[],'character':[],'ui_world':[],'other':[]}
for r in rows:
    s=r['summary'].lower()
    k=r['key']
    if k in {'DEV-3','DEV-4','DEV-5','DEV-6'}:
        cats['foundation'].append(r)
    elif k.startswith('DEV-2') and 'DB-NFR' in r['summary']:
        cats['db'].append(r)
    elif k in {'DEV-15','DEV-16','DEV-17','DEV-18','DEV-19','DEV-20','DEV-46','DEV-47','DEV-48','DEV-49','DEV-50','DEV-51','DEV-52','DEV-53','DEV-54','DEV-55','DEV-56','DEV-57','DEV-58'}:
        cats['auth_ui'].append(r)
    elif r['key'] in {'DEV-30','DEV-31','DEV-32','DEV-33','DEV-34','DEV-35','DEV-36','DEV-37','DEV-38','DEV-39','DEV-40','DEV-41','DEV-42','DEV-43','DEV-44','DEV-45'}:
        cats['character'].append(r)
    else:
        cats['other'].append(r)

print(json.dumps({'count':len(rows),'rows':rows,'categories':{k:[x['key'] for x in v] for k,v in cats.items()}}, indent=2))
