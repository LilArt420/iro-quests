import sys, json, re, collections
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata
n = luadata.load_any('/Users/arthurmartins/Projects/world-build/client-data/ig/navi_npc_us.lub', 'latin-1')['Navi_Npc']
iro_by_map = collections.defaultdict(list); iro_names = set()
GENERIC = {'guard', 'soldier', 'kafra employee', 'citizen', 'villager', 'merchant', 'adventurer', 'guide', 'boy', 'girl', 'man', 'woman', 'old man', 'traveler'}
for v in n.values():
    nm = re.sub(r'\s+', ' ', str(v[5])).strip()
    iro_by_map[v[1]].append((v[7], v[8], nm.lower())); iro_names.add(nm.lower())
srv = json.load(open('server_npcs.json'))
srv_by_map = collections.defaultdict(list); srv_names = collections.defaultdict(set)
for m, x, y, disp, name, f in srv:
    if 'world_sync_placeholders' in f: continue   # placeholders are not quests
    d = re.sub(r'^\[|\]$', '', disp).strip().lower()
    srv_by_map[m].append((x, y, d, f)); srv_names[d].add(f)
named_iro = sorted((x for x in iro_names if len(x) >= 5 and x not in GENERIC), key=len, reverse=True)
RX = re.compile(r'\b(' + '|'.join(map(re.escape, named_iro)) + r')\b', re.I)
def last(nm): return nm.lower().split()[-1] if nm.split() else nm.lower()
keys = json.load(open('keys.json'))
for q in keys:
    iro_hit = srv_hit = False; ev = []
    for nm, m, x, y in q['givers']:
        l = nm.lower()
        near_iro = [t for t in iro_by_map.get(m, []) if abs(t[0]-x) <= 4 and abs(t[1]-y) <= 4]
        if any(l in t[2] or t[2] in l or last(nm) == last(t[2]) for t in near_iro) or (l in iro_names and l not in GENERIC):
            iro_hit = True; ev.append('iro:' + nm)
        near_s = [t for t in srv_by_map.get(m, []) if abs(t[0]-x) <= 6 and abs(t[1]-y) <= 6]
        if any(l in t[2] or t[2] in l or last(nm) == last(t[2]) for t in near_s):
            srv_hit = True; ev.append('srv:' + nm + '@' + [t[3] for t in near_s if l in t[2] or t[2] in l or last(nm) == last(t[2])][0].split('/')[-1])
    if not q['givers']:
        for mm in set(x.lower() for x in RX.findall(q['text'])):
            iro_hit = True; ev.append('iro-text:' + mm)
            if mm in srv_names: srv_hit = True; ev.append('srv-text:' + mm + '@' + sorted(srv_names[mm])[0].split('/')[-1])
    q['iro_npc'] = iro_hit; q['srv_npc'] = srv_hit; q['ev'] = ev[:4]
json.dump(keys, open('keys.json', 'w'))
c = collections.Counter((q['pack'][:22], q['iro_npc'], q['srv_npc']) for q in keys)
for k, v in sorted(c.items()): print(k, v)
