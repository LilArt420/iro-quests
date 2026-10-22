"""City Investment (kRO 2015 "City Contribution", iRO "Merchant Union"): data for the mod.

Usage: python3 gen_union.py WORKDIR MODDIR
Reads WORKDIR/quests_client.json (the iRO client's quest text), mobs_small.json,
iro_mob_names.json, server_npcs2.json (live server NPCs) and the iRO navigation table.
Writes:
  MODDIR/db/when/city_investment/quest_db.yml          deliveries, receipts, wanted, union member
  MODDIR/npc/when/city_investment/union_data.txt       request tables for the board
  MODDIR/npc/when/city_investment/union_recipients.txt the delivery recipients
"""
import sys, os, re, json, collections
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata

W, M = sys.argv[1], sys.argv[2]
raw = json.load(open(os.path.join(W, 'quests_client.json')))['QuestInfoList']
mobs = json.load(open(os.path.join(W, 'mobs_small.json')))
byid = {v['id']: a for a, v in mobs.items()}
srv = json.load(open(os.path.join(W, 'server_npcs2.json')))
navi = luadata.load_any('/Users/arthurmartins/Projects/world-build/client-data/ig/navi_npc_us.lub', 'latin-1')['Navi_Npc']


def text(i):
    v = raw[str(i)]
    d = v.get('Description') or {}
    d = ' '.join(map(str, d.values())) if isinstance(d, dict) else str(d)
    return re.sub(r'<[^>]*>|\^[0-9a-fA-F]{6}', '', d)


ITEM = {'fly wing': 'Wing_Of_Fly', 'yggdrasil lea': 'Leaf_Of_Yggdrasil', 'white potion': 'White_Potion', 'magnif': 'Spectacles',
        'blue gemstone': 'Blue_Gemstone', 'butterfly wing': 'Wing_Of_Butterfly', 'orange potion': 'Orange_Potion',
        'elemental converter (water)': 'Elemental_Water', 'elemental converters (wind)': 'Elemental_Wind',
        'elemental converter (wind)': 'Elemental_Wind', 'silver arrow': 'Silver_Arrow', 'bouquet': 'Bunch_Of_Flowers',
        'red potion': 'Red_Potion', 'yellow potion': 'Yellow_Potion', 'meat': 'Meat', 'witherless rose': 'Witherless_Rose',
        'awakening potion': 'Awakening_Potion', 'berserk potion': 'Berserk_Potion', 'carrot': 'Carrot',
        'sweet potato': 'Sweet_Potato', 'holy water': 'Holy_Water', 'spicy sauce': 'Hot_Sauce', 'fire arrow': 'Fire_Arrow',
        'trap': 'Booby_Trap', 'green potion': 'Green_Potion', 'cotton shirt': 'Cotton_Shirt',
        "monsters' food": '528',   # Monster's_Feed: the apostrophe can't be a script constant
        'concentration': 'Center_Potion'}


def item_of(name):
    n = name.lower()
    for k in sorted(ITEM, key=len, reverse=True):
        if n.startswith(k) or k in n:
            return ITEM[k]
    raise SystemExit('no item for ' + name)


pat = re.compile(r'deliver (\d+) (.+?) to (.+?)\s+(?:at|in|Inside)\s+(?:the )?(.+?) ?\(\s*(\w+)\s*\).*?\(\s*(\d+)[ ,]+(\d+)\s*\)', re.I)
nav_at = collections.defaultdict(list)
for v in navi.values():
    nav_at[v[1]].append((v[7], v[8], str(v[5]).strip(), v[4], v[2]))
deliveries = []
for i in range(5497, 5725):
    v = raw.get(str(i))
    if not v or 'Receipt' in v['Title'] or 'Cool' in v['Title']:
        continue
    m = pat.search(text(i))
    if not m:
        raise SystemExit('unparsed %d %s' % (i, text(i)))
    n, item, who, place, mp, x, y = m.groups()
    cls = re.search(r'\((\w)-Delivery', v['Title']).group(1)
    # the iRO navigation entry at that spot gives the NPC's sprite
    nv = [t for t in nav_at[mp] if abs(t[0] - int(x)) <= 2 and abs(t[1] - int(y)) <= 2]
    sprite = nv[0][3] if nv else 0
    deliveries.append(dict(q=i, receipt=i + 1, cls=cls, count=int(n), item=item_of(item), who=who.strip(),
                           place=place.strip(), map=mp, x=int(x), y=int(y), sprite=sprite, navi=nv[0][4] if nv else 0))

# Wanted: weekly boss bounties (5471-5495).
ALIAS = {'entweihen crothen': 'ENTWEIHEN', 'unsealed baphomet': 'BAPHOMET_I', 'bakonawa': 'BAKONAWA_3', 'buwaya': 'BUWAYA',
         'amdarais': 'MG_AMDARAIS', 'faceworm queen': 'FACEWORM_QUEEN', 'celine kimi': 'XM_CELINE_KIMI',
         'morocc necromancer': 'EP14_MORS_BOSSA', 'reaper anku': 'GRIM_REAPER_ANKOU', 'morocc the despair god': 'MM_MOROCC_ADT',
         'grand pere': 'GRAND_PERE', 'charleston no': 'CHARLESTON3', 'sarah irene': 'MM_SARAH', 'crazy ferlock': 'E1_FELOCK',
         't_w_o': 'T_W_O', 'bijou': 'BIJOU', 'stefan j': 'AS_RAGGED_GOLEM', 'the shadow of nydhorgg': 'S_NYDHOG',
         'bangungot': 'BANGUNGOT_3', 'irene the wise elder': 'IRENE_ELDER', 'the torturous redeemer': 'TORTUROUS_REDEEMER'}
# Fenrir (Geffen Magic Tournament, switched off in rAthena) and the Wandering Purple Dragon (no such
# monster on the server) can't be hunted here, so their bounties are left out.
wanted, skipped = [], []
for i in range(5471, 5496):
    t = text(i)
    m = re.search(r'(?:defeats?|captures?|stops?) (?:the top boss of the Constellation, )?(.+?)(?:,| in | on | at |\.)', t)
    tok = int(re.search(r'(\d+)', raw[str(i)].get('Summary', '')).group(1))
    name = m.group(1).strip().lower() if m else '?'
    aeg = ALIAS.get(name)
    if i == 5487:
        aeg = 'E2_FELOCK'
    if not aeg or aeg not in mobs:
        skipped.append((i, name, aeg)); continue
    wanted.append(dict(q=i, mob=mobs[aeg]['id'], aegis=aeg, tokens=tok, text=t))
json.dump(dict(deliveries=deliveries, wanted=wanted, skipped=skipped), open(os.path.join(W, 'union_data.json'), 'w'), indent=1)
print('deliveries', collections.Counter(d['cls'] for d in deliveries), 'wanted', len(wanted), 'skipped', skipped)
print('no navi sprite:', [(d['q'], d['who'], d['map']) for d in deliveries if not d['sprite']])

# ---------------------------------------------------------------- mod files
def ascii(s):
    return s.encode('ascii', 'replace').decode().replace('"', "'")


TOKENS = {'A': 50, 'B': 30, 'C': 20}          # Inven 4255: A 50, B 30, C 20 Union Tokens
y = ['# iRO Quests: City Investment (iRO quest ids). Generated by tools/union/gen_union.py.',
     'Header:', '  Type: QUEST_DB', '  Version: 3', '', 'Body:',
     '  - Id: 12370', '    Title: "Member of Union"',
     '  - Id: 5470', '    Title: "(Wanted) Pending"', '    TimeLimit: Wednesday 4h']
for d in deliveries:
    y += ['  - Id: %d' % d['q'], '    Title: "(%s-Delivery Quest)"' % d['cls'],
          '  - Id: %d' % d['receipt'], '    Title: "(%s-Delivery Quest) Receipt"' % d['cls']]
for w in wanted:
    y += ['  - Id: %d' % w['q'], '    Title: "(Wanted)"', '    Targets:', '      - Mob: %s' % w['aegis'], '        Count: 1']
dbdir = os.path.join(M, 'db', 'when', 'city_investment'); os.makedirs(dbdir, exist_ok=True)
open(os.path.join(dbdir, 'quest_db.yml'), 'w').write('\n'.join(y) + '\n')

S = ['//===== Ragnarok Offline mod: iRO Quests =====================',
     '//= City Investment: the request tables (generated by',
     '//= tools/union/gen_union.py from the iRO client\'s quest text).',
     '//============================================================',
     '-\tscript\tIQ_UnionData\t-1,{', '\tend;', 'OnInit:']
for cls in 'ABC':
    ds = [d for d in deliveries if d['cls'] == cls]
    S.append('\t// %s-class deliveries: %d, %d Union Tokens each' % (cls, len(ds), TOKENS[cls]))
    S.append('\tsetarray $@iqu%s_q[0], %s;' % (cls, ', '.join(str(d['q']) for d in ds)))
    S.append('\tsetarray $@iqu%s_who$[0], %s;' % (cls, ', '.join('"%s"' % ascii(re.sub(r'^an? ', '', d['who'])) for d in ds)))
    S.append('\tsetarray $@iqu%s_where$[0], %s;' % (cls, ', '.join('"%s"' % ascii(d['place']) for d in ds)))
S.append('\t// Wanted (S-class), weekly: quest, boss, Union Tokens')
S.append('\tsetarray $@iquW_q[0], %s;' % ', '.join(str(w['q']) for w in wanted))
S.append('\tsetarray $@iquW_mob[0], %s;' % ', '.join(str(w['mob']) for w in wanted))
S.append('\tsetarray $@iquW_tok[0], %s;' % ', '.join(str(w['tokens']) for w in wanted))
S += ['\tend;', '}', '']
npcdir = os.path.join(M, 'npc', 'when', 'city_investment'); os.makedirs(npcdir, exist_ok=True)
open(os.path.join(npcdir, 'union_data.txt'), 'w').write('\n'.join(S))

R = ['//===== Ragnarok Offline mod: iRO Quests =====================',
     '//= City Investment: the delivery recipients, at the spots and with the',
     '//= looks of the iRO client (quest text + navigation table). Generated by',
     '//= tools/union/gen_union.py.',
     '//============================================================', '']
for d in deliveries:
    name = ascii(re.sub(r'^an? ', '', d['who']))
    name = name[0].upper() + name[1:]
    spr = d['sprite'] or 894
    R.append('%s,%d,%d,4\tscript\t%s#iqu%d\t%d,{' % (d['map'], d['x'], d['y'], name, d['q'], spr))
    R.append('\tcallfunc "F_IQ_UnionDeliver", %d, %s, %d, "%s";' % (d['q'], d['item'], d['count'], name))
    R.append('\tend;')
    R.append('}')
open(os.path.join(npcdir, 'union_recipients.txt'), 'w').write('\n'.join(R) + '\n')
print('wrote', len(deliveries), 'recipients;', 'navi ids:', ' '.join(str(d['navi']) for d in deliveries if d['navi']))
