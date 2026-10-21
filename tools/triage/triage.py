import sys, json, re, collections
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata
CD = '/Users/arthurmartins/Projects/world-build/client-data/'
nm = luadata.load_any(CD + 'ig/navi_map_us.lub', 'latin-1')['Navi_Map']
iro_maps = {v[1]: v[2] for v in nm.values()}
d = json.load(open('quests_client.json'))['QuestInfoList']
scripted = {int(k) for k in json.load(open('scripted_ids.json'))} | {int(k) for k in json.load(open('scripted_ids_loose.json'))}
NAVI = re.compile(r'<INFO>([\w@-]+),(\d+),(\d+)')
def clean(s): return re.sub(r'<[^>]*>', '', re.sub(r'\^[0-9a-fA-F]{6}', '', str(s or ''))).replace('\n', ' ')
rows = []
for k, v in d.items():
    k = int(k)
    desc = v.get('Description') or {}
    raw = ' '.join(str(desc[x]) for x in sorted(desc, key=lambda z: int(z))) if isinstance(desc, dict) else str(desc)
    maps = [m.group(1) for m in NAVI.finditer(raw + ' ' + str(v.get('Summary') or ''))]
    if v.get('NpcNavi'): maps.insert(0, v['NpcNavi'])
    rows.append(dict(id=k, title=clean(v['Title']).strip(), summary=clean(v.get('Summary')).strip(),
                     desc=clean(raw).strip(), maps=maps, scripted=k in scripted, cool='CoolTimeQuest' in v))
json.dump(rows, open('quests_rows.json', 'w'), ensure_ascii=False)
miss = [r for r in rows if not r['scripted']]
c = collections.Counter(r['maps'][0] if r['maps'] else '-' for r in miss)
print(len(miss), 'nomap', c['-'])
print(c.most_common(120))
print('not iro maps:', collections.Counter(m for m in c if m != '-' and m not in iro_maps))
