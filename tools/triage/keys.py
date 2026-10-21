"""Per missing permanent quest: a title key (chain name) and the giver/NPC names in its text."""
import json, re, collections
raw = json.load(open('quests_client.json'))['QuestInfoList']
tri = json.load(open('triage.json'))
NV = re.compile(r'<NAVI>\[?([^\]<]+?)\]?<INFO>([a-z][\w@-]*),(\d+),(\d+)')
def tkey(t):
    t = re.sub(r'\^[0-9a-fA-F]{6}', '', t)
    t = re.sub(r'\s*[-:(]?\s*(Cooldown|Cool ?time|Waiting|Wait|Rest|Standby|Again|Repeat|Hold|Completed?|Failed|Passed|Receipt)\)?\s*$', '', t, flags=re.I)
    t = re.sub(r'^\[[^\]]*\]\s*', '', t)
    t = re.sub(r'\s*(\(?\d+\)?|[IVX]+|Lv\.?\s*\d+)$', '', t).strip(' -:')
    return t
out = []
for r in tri:
    if r['kind'] not in ('story', 'daily', 'job'): continue
    if r['pack'] in ('iRO Bounty Boards',): continue
    v = raw[str(r['id'])]; d = v.get('Description') or {}
    txt = ' '.join(map(str, d.values() if isinstance(d, dict) else [d])) + ' ' + str(v.get('Summary') or '')
    givers = [(re.sub(r'\^[0-9a-fA-F]{6}', '', n).strip(), m, int(x), int(y)) for n, m, x, y in NV.findall(txt)]
    givers = [g for g in givers if not g[1].isupper()]
    out.append(dict(id=r['id'], title=v['Title'].strip(), key=tkey(v['Title'].strip()), area=r['area'], pack=r['pack'], kind=r['kind'],
                    givers=givers, text=re.sub(r'<[^>]*>', '', txt)))
json.dump(out, open('keys.json', 'w'))
keys = sorted({o['key'] for o in out if len(o['key']) >= 5} | {g[0] for o in out for g in o['givers'] if len(g[0]) >= 4})
json.dump(keys, open('wiki_keys.json', 'w'))
print(len(out), 'quests;', len({o['key'] for o in out}), 'title keys;', len(keys), 'search keys')
