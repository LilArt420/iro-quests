"""Triage the client quests the server has no script for.
In: quests_rows.json (triage.py), navi tables. Out: triage.tsv, triage_summary.json"""
import sys, json, re, collections
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata
CD = '/Users/arthurmartins/Projects/world-build/client-data/'
npcs = luadata.load_any(CD + 'ig/navi_npc_us.lub', 'latin-1')['Navi_Npc']
rows = json.load(open('quests_rows.json'))
rows.sort(key=lambda r: r['id'])

AREA = [  # (regex on map name, area)
 (r'^(prontera|prt_|prt$|pront)', 'Prontera'), (r'^(izlude|iz_|izlu2dun)', 'Izlude/Byalan'),
 (r'^(geffen|gef_|gefenia)', 'Geffen'), (r'^(payon|pay_)', 'Payon'), (r'^(morocc|moc_|moro_|que_job)', 'Morroc'),
 (r'^(alberta|alb|treasure|tur_)', 'Alberta/Turtle Is.'), (r'^(aldebaran|alde_|c_tower|clock_|alde)', 'Al De Baran'),
 (r'^(yuno|kh_|juperos|jupe_|ju_)', 'Juno'), (r'^(einbroch|einbech|ein_)', 'Einbroch'),
 (r'^(lighthalzen|lhz_|sp_|rgsr|lhz)', 'Lighthalzen'), (r'^(hugel|hu_|odin_|abyss_|tha_|thana_)', 'Hugel/Thanatos/Odin'),
 (r'^(rachel|ra_|ice_dun|que_rachel|que_thr|thor_|moro_)', 'Rachel'), (r'^(veins|ve_)', 'Veins'),
 (r'^(comodo|cmd_|beach_|com_|um_|umbala)', 'Comodo/Umbala'), (r'^(niflheim|nif_)', 'Niflheim'),
 (r'^(amatsu|ama_)', 'Amatsu'), (r'^(gonryun|gon_)', 'Kunlun'), (r'^(louyang|lou_)', 'Louyang'),
 (r'^(ayothaya|ayo_)', 'Ayothaya'), (r'^(xmas)', 'Lutie'), (r'^(moscovia|mosk_)', 'Moscovia'),
 (r'^(brasilis|bra_)', 'Brasilis'), (r'^(dewata|dew_)', 'Dewata'), (r'^(malangdo|mal_|ma_)', 'Malangdo'),
 (r'^(malaya|ma_)', 'Port Malaya'), (r'^(eclage|ecl_)', 'Eclage'), (r'^(mid_camp|man_|spl_|splendide|manuk|mid_|bif_|mora)', 'New World/Bifrost'),
 (r'^(dic_|dicastes)', 'El Dicastes'), (r'^(lasagna|lasa_)', 'Lasagna'), (r'^(har_|rockridge)', 'Rock Ridge'),
 (r'^(verus|oz_|rebel)', 'Verus/Phantasmagorika'), (r'^(glast|gl_)', 'Glast Heim'),
 (r'^(nameless|abbey)', 'Nameless Island'), (r'^(dali|1@)', 'Dimensional Gap/Instances'),
 (r'^(airport|airplane|lhz_airport|y_airport)', 'Airship'), (r'^(mjolnir|in_orcs|gw_|wolfvill|anthell|mag_)', 'Fields/Misc'),
 (r'^(t_garden)', 'Garden of Time'), (r'^(pub_cat)', 'Cat Hand'),
 (r'^(jor_|star_|hero_|ygg_|ch1|ch2|vr_|ab_|bl_|job4_|tim_|amicitia|varm|bio|ba_|icas|icecastle|rgsr|gl_cas01_|x_prt_evt)', 'KRO-ONLY'),
]
def area_of(m):
    for rx, a in AREA:
        if re.match(rx, m): return a
    return None

# NPC names -> map (only names unique to one map, >= 5 chars)
nmap = collections.defaultdict(set)
for v in npcs.values():
    n = str(v[5]).strip()
    if len(n) >= 5 and not n.startswith('#'): nmap[n].add(v[1])
npc_unique = {n: next(iter(ms)) for n, ms in nmap.items() if len(ms) == 1}
NPCRX = re.compile(r'\b(' + '|'.join(sorted((re.escape(n) for n in npc_unique), key=len, reverse=True)) + r')\b')
TOWNS = {'Prontera': 'prontera', 'Izlude': 'izlude', 'Geffen': 'geffen', 'Payon': 'payon', 'Morroc': 'morocc', 'Morocc': 'morocc',
 'Alberta': 'alberta', 'Al De Baran': 'aldebaran', 'Aldebaran': 'aldebaran', 'Juno': 'yuno', 'Yuno': 'yuno', 'Einbroch': 'einbroch',
 'Einbech': 'einbech', 'Lighthalzen': 'lighthalzen', 'Hugel': 'hugel', 'Rachel': 'rachel', 'Veins': 'veins', 'Comodo': 'comodo',
 'Umbala': 'umbala', 'Niflheim': 'niflheim', 'Nifflheim': 'niflheim', 'Amatsu': 'amatsu', 'Kunlun': 'gonryun', 'Louyang': 'louyang',
 'Ayothaya': 'ayothaya', 'Lutie': 'xmas', 'Moscovia': 'moscovia', 'Brasilis': 'brasilis', 'Dewata': 'dewata', 'Malangdo': 'malangdo',
 'Port Malaya': 'malaya', 'Malaya': 'malaya', 'Eclage': 'eclage', 'Splendide': 'splendide', 'Manuk': 'manuk', 'Mora': 'mora',
 'El Dicastes': 'dicastes', 'Dicastes': 'dicastes', 'Lasagna': 'lasagna', 'Rock Ridge': 'rockridge', 'Verus': 'verus04',
 'Glast Heim': 'glast_01', 'Thanatos': 'tha_t01', 'Odin': 'odin_tem01', 'Byalan': 'izlu2dun', 'Turtle Island': 'tur_dun01',
 'Kiel Hyre': 'kh_', 'Juperos': 'juperos', 'Biolab': 'lhz_', 'Clock Tower': 'c_tower1', 'Sphinx': 'moc_', 'Pyramid': 'moc_',
 'Nameless Island': 'nameless_n', 'Issgard': 'icecastle', 'Jormungandr': 'jor_', 'Star Forest': 'star_', 'Varmundt': 'varm',
 'Amicitia': 'amicitia', 'Biosphere': 'bio', 'Varmundt': 'varm', 'Issgard': 'icecastle', 'Barmund': 'ba_', 'Regenschirm': 'rgsr', 'Yggdrasil': 'ygg_', 'Biosphere': 'bio', 'Abyss': 'ab_', 'Illusion': '1@', 'Endless Tower': '1@', 'Eden Group': 'moc_para01'}
TOWNRX = re.compile(r'\b(' + '|'.join(sorted(map(re.escape, TOWNS), key=len, reverse=True)) + r')\b')

EVENT = re.compile(r"\b(19|20)\d\d\b|Halloween|Christmas|X-?mas|Valentine|White Day|Easter|Thanksgiving|Turkey|Mother'?s Day|Father'?s Day|"
  r"St\.? ?Patrick|Anniversary|Lunar New Year|New Year|Chuseok|Songkran|Harvest Festival|Summer Festival|Winter Festival|Noodle|Sweets Festival|"
  r"Egg Festival|Flower Event|Snow Flower|Melon Festival|Popcorn|Booster Event|Royal Hunt|Battle ?Pass|Collaboration|\bRWC\b|Pirate Day|"
  r"Talk like a Pirate|Spotlight|Ferus Faire|Poring Con|Sports Festa|April Fool|Raffle|Independence Day|Dano|\[Event\]|Event\b|Festival|Shiba|"
  r"Season ?\d|S3 |Night Market|Ragnarok Tactics|Tactical Games|Trip to Another World|Glitch in Time|Tarnished Lamp|Spooky Machine|Romero|Ghouliet|"
  r"Unity Project|Rune Midgard Exposition|Mr\. Brando|Fireworks|Holmes|Ai On the Run|Ghoulish|Nightmare on Prontera|"
  r"Collab|Kumamon|Eggman|Chao\b|Sonic|Baby Shark|Grandpa Shark|Chocolat|Cocoa|Cacao|Sweets Drops|Happy Egg|Happy Clover|Happy Almond|Happy Cutepet|Happy Walk|"
  r"Happy Lunatic|Happy Poring|Happy Young|Happy Deviruchi|Rudolf|Santa|Snow ?Flower|Snow Boy|Festa Card|stamp book|stamp for|Dessert Class|Royal Hunt|"
  r"Angel's Side|Devil's Side|Fire Festival|Ocean Week|Kritura Souvenir|Hot Monster Hunt|Galactor|Bird Missile|Berg Ka|Hiccup|Toothless|Ruffnut|Tuffnut|"
  r"Candy|Cotton Candy|Night Market|Mysterious Toy|Noodle|Dumpling|Melon|Watermelon|Pumpkin|Ghost ?busters|Trick or Treat|Turkey|Pilgrim|Thanks|"
  r"Suspicious Babe|Paychecks|Small Wooden Boxes|Valfreyja Challenge|Gloria Challenge|Take a walk with Pet|Pet Walk|Shifu|Zhen's Trading|Moon ?cake|Hanbok|"
  r"Happiness sharing|sharing warm|sweet happiness|Share Sweetness|Delivery Confirmation|Delivered to |Delivery and Collection|Back to School|Unfortunate Cupid|"
  r"Detonation|Blood in Prontera|Day of the Dead|Nifflheim Tourists|Nifflheim Timer|Ectoplasm|Ecto Exterminators|Episode Ragnarok|Littlest Isis|Fae Crossed|Nyah|Humbug|"
  r"Supermundane|Sleigh|Ragnarok Of Love|Pub Crawler|Toilet Paper|Strange Kafra|Sewer Ghost|Happy Pet|Knuckles|Rabbit Hole|Evil Genius|Lurking Shadow|Kidnapped Monsters|"
  r"Inside Eggman|Mysterious Chao|End of an Adventure|Slot Machine|Claw Machine|Fishing Machine|Spirit Cleansing|Lullaby|Pirate Style|Raiders of the Lost|Bone Business|"
  r"Chair Situation|Out of Place|Dimensional Investigat|Event Pass|Forgotten Time Hunt|Firecracker|Lantern|Red Envelope|Lucky Bag|Fortune|Bingo|Lottery|Treasure Hunt Event|Rok Star|Poring Race|Monster Race|Summer|Winter Sports|Midsummer", re.I)
HIDDEN = re.compile(r'^(Invisible Quest|Blank|Place ?Holder|Test ?\d*|\d+|)$', re.I)
COOL = re.compile(r'Cooldown|Cool Down|Waiting|\bWait\b|\bRest\b|Standby|Resets? at|Reset at|04:00|reset|\bdelay\b|\[Wait\]|- ?Rest$|Time Limit|Rest Time', re.I)
DAILY = re.compile(r'\[Daily\]|daily|Board|Bounty|Hunting Board|Request Board|Monster Extermination|Eden Group|\bHunt(ing)?\b', re.I)
JOB = re.compile(r'Job Change|Job Quest|Job Test|Skill Quest|Rebirth|Transcend|Application for the|^Path of (the )?(Sky|Ascetic|Soul Reaper|Inquisitor|Night Watch|Meister|Spirit|Biolo|Dragon|Abyss|Imperial|Elemental|Cardinal|Troubadour|Trouvere|Shinkiro|Shiranui|Hyper|Star|Sky Emperor)|Change to |Hyper Novice|Novice.s Memories|Arch Mage|Elemental Master|Inquisitor|Soul Ascetic|Night Watch|Sky Emperor|Shinkiro|Shiranui|Spirit Handler|Biolo|Abyss Chaser|Dragon Knight|Imperial Guard|Cardinal|Troubadour|Trouvere|Meister|Hyper Novice|4th job|Expanded Super|Ninja training|Gunslinger|Rebel|Taekwon|Star Emperor|Soul Reaper|Kagerou|Oboro|Summoner|Doram', re.I)

out = []
for r in rows:
    if r['scripted']: continue
    t = r['title']; text = ' '.join([t, r['summary'], r['desc']])
    maps = [m for m in r['maps'] if not m.isupper()]
    src = 'navi' if maps else ''
    if not maps:
        m = NPCRX.search(text)
        if m: maps = [npc_unique[m.group(1)]]; src = 'npc:' + m.group(1)
    if not maps:
        m = TOWNRX.search(text)
        if m: maps = [TOWNS[m.group(1)]]; src = 'town:' + m.group(1)
    r2 = dict(id=r['id'], title=t, map=maps[0] if maps else '', src=src, summary=r['summary'], desc=r['desc'])
    if HIDDEN.match(t.strip()): kind = 'hidden'
    elif EVENT.search(t) or EVENT.search(r['desc'][:200]) and re.search(r'event', r['desc'], re.I): kind = 'event'
    elif COOL.search(t) or (COOL.search(r['summary']) and not r['desc'][:1].isalpha() is False and len(r['desc']) < 160 and re.search(r'again|cooldown|wait', r['desc'], re.I)): kind = 'cooldown'
    elif JOB.search(t): kind = 'job'
    elif DAILY.search(t) or r['cool'] or re.search(r'daily quest|repeatable|once a day|every day', r['desc'], re.I): kind = 'daily'
    else: kind = 'story'
    r2['kind'] = kind
    out.append(r2)

# inherit maps from neighbours: same title first, then nearest id within 4 that shares a title word
bytitle = collections.defaultdict(list)
for r in out: bytitle[r['title']].append(r)
for t, rs in bytitle.items():
    ms = collections.Counter(r['map'] for r in rs if r['map'])
    if ms:
        for r in rs:
            if not r['map']: r['map'] = ms.most_common(1)[0][0]; r['src'] = 'same-title'
for i, r in enumerate(out):
    if r['map']: continue
    for d in (1, -1, 2, -2, 3, -3, 4, -4):
        j = i + d
        if 0 <= j < len(out) and out[j]['map'] and abs(out[j]['id'] - r['id']) <= 6:
            r['map'] = out[j]['map']; r['src'] = 'neighbour:%d' % out[j]['id']; break
for r in out:
    a = area_of(r['map']) if r['map'] else None
    if r['map'] in ('dicastes', 'manuk', 'splendide'): a = 'El Dicastes' if r['map'] == 'dicastes' else 'New World/Bifrost'
    r['area'] = a or ('?' if not r['map'] else 'Other:' + r['map'])
    if r['area'] == 'KRO-ONLY': r['kind'] = 'kro-only:' + r['kind']
# event families (cooldown/hidden near an event inherit "event")
for i, r in enumerate(out):
    if r['kind'] in ('cooldown', 'hidden'):
        for d in (-1, 1, -2, 2):
            j = i + d
            if 0 <= j < len(out) and out[j]['kind'] == 'event' and abs(out[j]['id'] - r['id']) <= 3:
                r['kind'] = 'event'; break
with open('triage.tsv', 'w') as f:
    f.write('id\tkind\tarea\tmap\ttitle\tmap_source\tsummary\tdescription\n')
    for r in out:
        f.write('\t'.join(str(r[k]).replace('\t', ' ') for k in ('id', 'kind', 'area', 'map', 'title', 'src', 'summary', 'desc')) + '\n')
kinds = collections.Counter(r['kind'] for r in out)
print(kinds)
perm = [r for r in out if r['kind'] in ('story', 'daily', 'job')]
print('permanent', len(perm), 'distinct titles', len({r['title'] for r in perm}))
ac = collections.Counter(r['area'] for r in perm)
act = collections.defaultdict(set)
for r in perm: act[r['area']].add(r['title'])
for a, n in ac.most_common(): print(f'{a:35} {n:5} ids  {len(act[a]):4} titles')

# --- does the quest-giver already exist on the server? ---
srv = json.load(open('server_npcs.json'))
bymap = collections.defaultdict(list)
for m, x, y, disp, name, f in srv: bymap[m].append((x, y, disp.lower(), f))
raw = json.load(open('quests_client.json'))['QuestInfoList']
NV = re.compile(r'<NAVI>\[([^\]]+)\]<INFO>([a-z][\w@-]*),(\d+),(\d+)')
def npc_status(qid):
    v = raw[str(qid)]
    d = v.get('Description') or {}
    txt = ' '.join(str(x) for x in (d.values() if isinstance(d, dict) else [d])) + str(v.get('Summary') or '')
    hits = []
    for name, m, x, y in NV.findall(txt):
        name = re.sub(r'\^[0-9a-fA-F]{6}', '', name).strip().lower()
        x, y = int(x), int(y)
        near = [s for s in bymap.get(m, []) if abs(s[0] - x) <= 6 and abs(s[1] - y) <= 6]
        named = [s for s in bymap.get(m, []) if name and (name in s[2] or s[2] in name) and len(s[2]) > 2]
        hits.append('named' if named else 'near' if near else 'none')
    if not hits: return ''
    return 'named' if 'named' in hits else 'near' if 'near' in hits else 'none'
for r in out: r['npc'] = npc_status(r['id'])
with open('triage.tsv', 'w') as f:
    f.write('id\tkind\tarea\tmap\tnpc_on_server\ttitle\tmap_source\tsummary\tdescription\n')
    for r in out:
        f.write('\t'.join(str(r[k]).replace('\t', ' ') for k in ('id', 'kind', 'area', 'map', 'npc', 'title', 'src', 'summary', 'desc')) + '\n')
print(collections.Counter((r['kind'], r['npc']) for r in out if r['kind'] in ('story', 'daily')))
json.dump(out, open('triage.json', 'w'), ensure_ascii=False)

# --- content packs ---
def pack(r):
    i, t = r['id'], r['title']
    if r['kind'].startswith('kro-only'): return 'kRO-only maps (other session)'
    if r['kind'] == 'event': return 'Retired events'
    if t.startswith('Bounty Board'): return 'iRO Bounty Boards'
    if 60000 <= i < 60900 and re.search(r'Hunt|Extermination|Timer', t): return 'iRO Gramps weekly turn-ins'
    if 21000 <= i < 21900: return 'Town & field quests (2021 revamp)'
    if 21900 <= i < 22000: return 'New adventurer story (Leno, Jewel of Helion)'
    if i < 200 or 23000 <= i < 23100: return 'Criatura Academy'
    if 40000 <= i < 80000 or i >= 290000: return 'iRO original quests'
    return 'Older kRO quests (1000-19999)'
for r in out: r['pack'] = pack(r)
json.dump(out, open('triage.json', 'w'), ensure_ascii=False)
with open('triage.tsv', 'w') as f:
    f.write('id\tpack\tkind\tarea\tmap\tnpc_on_server\ttitle\tmap_source\tsummary\tdescription\n')
    for r in out:
        f.write('\t'.join(str(r[k]).replace('\t', ' ') for k in ('id', 'pack', 'kind', 'area', 'map', 'npc', 'title', 'src', 'summary', 'desc')) + '\n')
PERM = ('story', 'daily', 'job')
pk = collections.defaultdict(lambda: collections.Counter())
for r in out: pk[r['pack']][r['kind'].split(':')[-1]] += 1
print('\nPACK TOTALS')
for p, c in sorted(pk.items(), key=lambda x: -sum(x[1].values())):
    print(f"{p:45} total {sum(c.values()):5}  " + ' '.join(f'{k}={v}' for k, v in c.most_common()))
pa = collections.defaultdict(collections.Counter)
for r in out:
    if r['kind'] in PERM: pa[r['area']][r['pack']] += 1
print('\nAREA x PACK (permanent only)')
for a, c in sorted(pa.items(), key=lambda x: -sum(x[1].values()))[:25]:
    print(f"{a:28} {sum(c.values()):4}  " + ' | '.join(f'{k[:22]}={v}' for k, v in c.most_common()))
