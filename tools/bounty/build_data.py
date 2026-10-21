"""Build the Bounty Board data: boards (iRO client navi) and their quests
(iRO client quest table), each quest's monster resolved to the server's mob_db.
Usage: python3 build_data.py WORKDIR  -> WORKDIR/bounty_data.json"""
import sys, os, re, json, collections
W = sys.argv[1]
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata
CD = '/Users/arthurmartins/Projects/world-build/client-data/ig/'
quests = json.load(open(os.path.join(W, 'quests_client.json')))['QuestInfoList']
mobs = json.load(open(os.path.join(W, 'mobs_small.json')))           # aegis -> info
byid = {v['id']: a for a, v in mobs.items()}
iro = collections.defaultdict(set)                                  # iRO monster name -> ids
for v in luadata.load_any(CD + 'navi_mob_us.lub', 'latin-1')['Navi_Mob'].values():
    iro[re.sub(r'\s+', ' ', str(v[5])).strip().lower()].add(int(v[4]) & 0xffff)
srvname = collections.defaultdict(set)
for a, v in mobs.items():
    if v['name']: srvname[v['name'].lower()].add(v['id'])

# Names in the quest text that neither table spells the same way.
ALIAS = {
 'snake': 1025, 'sidewinder': 1037, 'skel worker': 1169, 'arclouse': 1194,
 'wickbine tres': 1653, 'bewler': None, 'ferus': 1714,
 'rake horn scaraba': 2086, 'rake scaraba': 2086, 'horn scaraba': 2084, 'uni-horn scaraba': 2083, 'antler scaraba': 2085,
 'worm tail': 1024, 'picky egg': 1050, 'nightmare minorous': 2353, 'nightmare verit': 2355, 'nightmare mimic': 2356,
 'charge basilisk': 3504, 'combat basilisk': 3503, 'jungle mandragora': 3506, 'fur seal': 1317, 'seal': 1317,
 'cookie': 1265, 'cookie (red)': 1246, 'deleter (ground)': 1385, 'deleter (sky)': 1384, 'ground deleter': 1385, 'flying deleter': 1384,
 'venatu (blue)': 1679, 'venatu (orange)': 1678, 'venatu (purple)': 1676, 'venatu (green)': 1677,
 'purple venatu': 1676, 'green venatu': 1677, 'orange venatu': 1678, 'blue venatu': 1679,
 'cenere (green)': 3247, 'cenere': 2365, 'kobold (axe)': 1133, 'kobold (hammer)': 1134, 'kobold (mace)': 1135,
 'axe kobold': 1133, 'hammer kobold': 1134, 'mace kobold': 1135, 'novus (red)': 1715, 'novus (yellow)': 1718,
 'red novus': 1715, 'yellow novus': 1718, 'deathword': 1698, 'death word': 1698, 'acidus (blue)': 1716, 'acidus (gold)': 1713,
 'blue acidus': 1716, 'gold acidus': 1713, 'ferus (red)': 1714, 'ferus (green)': 1717,
 'lichtern (blue)': 2367, 'lichtern (yellow)': 2368, 'lichtern (red)': 2369, 'lichtern (green)': 2370,
 'blue lichtern': 2367, 'yellow lichtern': 2368, 'red lichtern': 2369, 'green lichtern': 2370,
 'matte drainliar': 3750, 'knife goblin': 1122, 'female thief bug': 1053, 'male thief bug': 1054,
 'flying petite': 1156, 'ground petite': 1155, 'cursed box': 2479, 'cursed book': 2478,
 'alligator': 1271, 'goat': 1372, 'harpy': 1376, 'skeleton': 1076, 'soldier skeleton': 1028, 'archer skeleton': 1016,
 'munak': 1026, 'bongun': 1188, 'spore': 1014, 'bigfoot': 1060, 'elder willow': 1033, 'picky': 1049,
 'chen lio': 2224, 'flamel emure': 2222,
 # "Nightmare" Biolab bounties are the Biolab 5 (V_) monsters: their EXP x 150 is iROWiki's 160-175 board.
 'nightmare kathryne keyron': 3210, 'nightmare margaretha sorin': 3209, 'nightmare cecil damon': 3211, 'nightmare eremes guile': 3208,
 'nightmare seyren windsor': 3213, 'nightmare howard alt-eisen': 3212, 'nightmare randel lawrence': 3226, 'nightmare flamel emure': 3227,
 'nightmare celia alde': 3228, 'nightmare chen lio': 3229, 'nightmare gertie': 3230, 'nightmare alphoccio': 3231, 'nightmare trentini': 3232,
 'poison spore': 1077, 'dark priest': 1198, 'egnigem cenia': 1652, 'freezer': 1319,
 'elder greatest general': 1277,
}
# Restless Dead: three variants, one quest each (63746-63748), in id order.
RESTLESS = {63746: 3751, 63747: 3752, 63748: 3753}

def resolve(qid, name):
    n = name.strip().lower()
    if qid in RESTLESS: return RESTLESS[qid], 'restless'
    if n in ALIAS: return ALIAS[n], 'alias'
    ids = iro.get(n) or set()
    ids = {i for i in ids if i in byid}
    if len(ids) == 1: return next(iter(ids)), 'iro-navi'
    ids = {i for i in srvname.get(n, set())
           if not re.match(r'(G_|MD_|A_|T_|EVENT_|MIN_|ABI_|CP_|BIO_|W_|E_|C\d_|M_|J_|META_|ECO_|VR_)', byid[i])}
    if len(ids) == 1: return next(iter(ids)), 'server-name'
    return None, 'unresolved %s' % sorted(ids)

# Boards from the iRO navigation table (sprite 837 "Bounty Board <lo>-<hi>").
boards = []
for v in luadata.load_any(CD + 'navi_npc_us.lub', 'latin-1')['Navi_Npc'].values():
    m = re.match(r'Bounty Board (\d+)-(\d+)$', str(v[5]))
    if v[4] == 837 and m and v[1] != 'prontera' or (v[1] == 'prontera' and m and v[7] < 150):
        boards.append(dict(map=v[1], x=v[7], y=v[8], lo=int(m.group(1)), hi=int(m.group(2)), navi=v[2]))
boards.sort(key=lambda b: (b['map'], b['lo']))
TOWN = {  # quest text "return to ..." -> board map
 'Prontera Center Fountain': 'prontera', 'Izlude': 'izlude', 'Geffen': 'geffen', 'Payon': 'payon', 'Alberta': 'alberta',
 'Morroc': 'morocc', 'Aldebaran': 'aldebaran', 'Lutie': 'xmas', 'Comodo': 'comodo', 'Umbala': 'umbala', 'Niflheim': 'niflheim',
 'Malangdo': 'malangdo', 'Lasagna': 'lasagna', 'Juno': 'yuno', 'Lighthalzen': 'lighthalzen', 'Einbroch': 'einbroch',
 'Hugel': 'hugel', 'Rachel': 'rachel', 'Veins': 'veins', 'Verus City': 'verus04', 'Manuk': 'manuk', 'El Dicastes': 'dicastes01',
 'Splendide': 'splendide', 'Mora': 'mora', 'Eclage': 'ecl_in01', 'Illusion of Moonlight Dungeon': 'pay_d03_i',
 'Illusion of Vampire Dungeon': 'gef_d01_i', 'Illusion of Frozen Dungeon': 'ice_d03_i'}
pat = re.compile(r'Hunt (\d+) (.+?) monsters? and return to (.+?)\s*$')
qs, skipped = [], []
for k in sorted(int(x) for x in quests):
    v = quests[str(k)]
    if not v['Title'].startswith('Bounty Board'): continue
    desc = ' '.join(v['Description'].values()).strip()
    m = pat.search(desc)
    name = m.group(2).strip() if m else v['Title'][len('Bounty Board '):].strip()
    ret = m.group(3) if m else 'the Bounty Board at Aldebaran'
    town = re.sub(r"^.*?\b(at|in|near) (the )?(center of )?", '', ret)
    mp = TOWN.get(town)
    if v['Title'].strip() == 'Bounty Board' or not mp:
        skipped.append(dict(id=k, name=name, why='no board for "%s"' % ret)); continue
    mid, how = resolve(k, name)
    if not mid:
        skipped.append(dict(id=k, name=name, why='monster not on the server (%s)' % how)); continue
    qs.append(dict(id=k, name=name, mob=mid, aegis=byid[mid], lv=mobs[byid[mid]]['lv'], map=mp, set='B' if k >= 63000 else 'A',
                   title=v['Title'].strip(), desc=desc, how=how))
# iRO replaced most towns' boards with the 63xxx set. The older 62xxx quests stay only
# where a town never got the new set, or where iROWiki still lists the monster there.
FULL_A = {'prontera', 'geffen', 'payon'}
A_EXTRA = {('yuno', 1676), ('yuno', 1677), ('yuno', 1678), ('yuno', 1679), ('yuno', 1365)}
b_towns = {q['map'] for q in qs if q['set'] == 'B'}
for q in list(qs):
    if q['set'] == 'A' and q['map'] in b_towns and q['map'] not in FULL_A and (q['map'], q['mob']) not in A_EXTRA:
        qs.remove(q); skipped.append(dict(id=q['id'], name=q['name'], why='older set, replaced at this town'))
# One quest per monster per town: the newer (63xxx) set wins, else the lowest id.
keep, seen = [], {}
for q in sorted(qs, key=lambda q: (q['set'] != 'B', q['id'])):
    key = (q['map'], q['mob'])
    if key in seen:
        skipped.append(dict(id=q['id'], name=q['name'], why='same monster as %d at this board' % seen[key])); continue
    seen[key] = q['id']; keep.append(q)
# Each quest goes to the board of its town whose level range holds the monster's level, else the nearest one.
for q in keep:
    bs = [b for b in boards if b['map'] == q['map']]
    if q['map'] == 'manuk' and 'scaraba' in q['aegis'].lower():   # iROWiki: Scarabas are on the 140-160 board
        bs = [b for b in bs if b['lo'] == 140]
    inside = [b for b in bs if b['lo'] <= q['lv'] <= b['hi']]
    b = min(inside, key=lambda b: b['hi'] - b['lo']) if inside else min(bs, key=lambda b: min(abs(q['lv'] - b['lo']), abs(q['lv'] - b['hi'])))
    q['board'] = (b['map'], b['x'], b['y'])
    b.setdefault('quests', []).append(q['id'])
keep.sort(key=lambda q: q['id'])
boards = [b for b in boards if b.get('quests')]
json.dump(dict(boards=boards, quests=keep, skipped=sorted(skipped, key=lambda s: s['id'])), open(os.path.join(W, 'bounty_data.json'), 'w'), indent=1)
print('boards', len(boards), 'quests', len(keep), 'skipped', len(skipped))
for b in boards: print(' ', b['map'], b['x'], b['y'], f"{b['lo']}-{b['hi']}", len(b.get('quests', [])))
for s in sorted(skipped, key=lambda s: s['id']):
    if not s['why'].startswith('same'): print('  skip', s)
print('dups dropped', sum(1 for s in skipped if s['why'].startswith('same')))
