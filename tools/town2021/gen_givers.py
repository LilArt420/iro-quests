"""Town quests (2021 revamp): the dungeon-daily givers of iRO's 2022 series.

Usage: python3 gen_givers.py WORKDIR MODDIR
Each giver hands out mod eden-rework-2021's missions (same quest ids, cooldowns, kill
counts and rewards: its S_Row table) from the NPC iRO places in the field. Positions,
looks and names are the iRO navigation table's; the quest log entries are copied from
that mod's quest_db, so they work with it switched off. iRO's "...Again" repeats of the
same hunts are the board's and are left out.
Writes npc/when/town_quests_2021/dungeon_dailies.txt and the section of
db/when/town_quests_2021/quest_db.yml between the GENERATED markers.
"""
import sys, os, re, json
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata

W, M = sys.argv[1], sys.argv[2]
EDEN = os.path.expanduser('~/Library/Application Support/Ragnarok Offline/state/mods/eden-rework-2021')
raw = json.load(open(os.path.join(W, 'quests_client.json')))['QuestInfoList']
navi = {v[2]: v for v in luadata.load_any('/Users/arthurmartins/Projects/world-build/client-data/ig/navi_npc_us.lub', 'latin-1')['Navi_Npc'].values()}
rows = {}
for m in re.finditer(r'callsub S_Row, (\d+), (\d+), (\d+), (\d+), "([^"]*)", "((?:[^"\\]|\\.)*)", "((?:[^"\\]|\\.)*)", (\d+), (\d+), (\d+), "([^"]*)", "([^"]*)";',
                     open(os.path.join(EDEN, 'npc', 'eden_paradise_missions.txt')).read()):
    g = m.groups()
    rows[int(g[1])] = dict(cd=int(g[2]), lv=int(g[3]), title=g[5].replace('\\"', "'"), bexp=int(g[7]), jexp=int(g[8]),
                           coin=int(g[9]), items=g[10], rewards=g[11])
eden_q = {}
for b in re.split(r'\n(?=  - Id: )', open(os.path.join(EDEN, 'db', 'quest_db.yml')).read()):
    m = re.match(r'  - Id: (\d+)', b)
    if m:
        eden_q[int(m.group(1))] = b.rstrip()

# navi id, script name suffix, intro record (or 0), greeting lines, missions
GIVERS = [
    (14045, 'iqodin', 21581, ["Odin Temple, east of here. The monsters", "there grow bolder every day. Will you", "take a hand?"], [21582, 21585, 21588]),
    (14041, 'iqbio', 21591, ["^777777The ashes of a campfire. Under a", "stone, a note: \"The souls in the Bio", "Lab deserve rest. Grant it to them.\"^000000"],
     [21592, 21595, 21598, 21601, 21604, 21607, 21610, 21613, 21616, 21619, 21622, 21625]),
    (14042, 'iqmag1', 21628, ["The Monster Museum needs specimens from", "the Magma Dungeon. Will you help?"], [21629, 21632, 21635]),
    (14043, 'iqmag2', 21628, ["Back from the Magma Dungeon? The", "museum still needs specimens."], [21629, 21632, 21635]),
    (14046, 'iqtha1', 21649, ["The lower floors of Thanatos Tower are", "a museum of horrors. Help me clear", "them?"], [21651, 21654, 21657, 21660, 21663, 21666]),
    (14047, 'iqtha2', 21650, ["The upper floors are worse. Much worse.", "Are you strong enough?"], [21669, 21672, 21675, 21678]),
    (14039, 'iqgl1', 21681, ["Glast Heim Castle crawls with lost", "souls. Purify them, child."], [21683, 21686, 21689, 21692, 21695]),
    (14040, 'iqgl2', 21682, ["The chivalry halls of Glast Heim. The", "knights there never stopped fighting."], [21698, 21701, 21704, 21707]),
    (14036, 'iqdim1', 21710, ["The other world, beyond the rift. The", "expedition needs hunters."], [21713, 21716, 21719, 21722, 21725, 21728, 21731, 21734, 21737]),
    (14037, 'iqdim2', 21711, ["You again! Good. The expedition always", "needs hands. What'll it be?"], [21740, 21743, 21746, 21749, 21752, 21755, 21758, 21761, 21764]),
    (14038, 'iqdim3', 21712, ["Mora is peaceful, mostly. The little", "ones in the forest, though..."], [21767, 21770]),
    (14044, 'iqlartal', 0, ["The incarnations of Morocc still walk", "the land. They must be put down."], [21774, 21777, 21780, 21783]),
    (14026, 'iqnl', 0, ["The dead walk this island. Help me", "cleanse it."], [21363, 21365, 21367]),
    (14027, 'iqra1', 0, ["A hidden passage has opened into the", "temple's sanctuary. It must be", "cleansed, area by area."], [21369, 21371, 21373]),
    (14014, 'iqra2', 0, ["Kobolds and Hill Winds, all over the", "plains. Nobody can farm like this."], [21375, 21377]),
    (14015, 'iqra3', 0, ["Kobold fur makes the warmest", "blankets. Hard to come by, though."], [21379]),
    (14016, 'iqra4', 0, ["I want to farm, but the weeds here", "fight back!"], [21381]),
    (14017, 'iqra5', 0, ["Magmalings from the volcano, right", "outside Veins. We need help."], [21383]),
    (14018, 'iqra6', 0, ["Desert Wolves, a whole pack of them.", "Hunt with me?"], [21385]),
    (14019, 'iqra7', 0, ["Ice Hearts make the most refreshing", "dishes. Bring me some?"], [21387]),
    (14020, 'iqra8', 0, ["My friend the wizard sent me to study", "the ice. The Snowiers won't let me."], [21389, 21391]),
]


def asc(s):
    return s.encode('ascii', 'replace').decode().replace('"', "'")


def menu_name(q):
    t = rows[q]['title']
    return asc(t if len(t) <= 34 else t[:33] + '.') + ' (daily)'


out = ['//===== Ragnarok Offline mod: iRO Quests =====================',
       '//= Dungeon dailies of iRO\'s 2022 series (kRO\'s 2021 town quest revamp)',
       '//===== Description: =========================================',
       '//= The field NPCs who hand out the Eden Group\'s dungeon missions on',
       '//= iRO: Morvand (Odin Temple), the campfire traces (Bio Lab), the',
       '//= Museum Staff (Magma Dungeon), Avril and Tart (Thanatos Tower),',
       '//= Darkess and Chiab (Glast Heim), Yerne, Theodore and Niu Niu',
       '//= (the other world), Lartal (Morocc\'s incarnations), Rotert (Nameless',
       '//= Island) and the Rachel and Veins askers (Tebenio, Harim, Cheddar,',
       '//= Minae, the Vigilante, Sarim, Tarim, the Magician\'s Friend). Same quest',
       '//= ids, cooldowns, kill counts and rewards (EXP, Eden Coins) as mod',
       '//= eden-rework-2021\'s mission boards. NPCs and positions are the',
       '//= iRO client\'s (navigation table, quest text 21363-21391, 21581-21784).',
       '//= Generated by tools/town2021/gen_givers.py.',
       '//============================================================', '']
qids = set()
for nid, suf, intro, greet, missions in GIVERS:
    v = navi[nid]
    name = asc(v[5])
    out.append('%s,%d,%d,%d\tscript\t%s#%s\t%d,{' % (v[1], v[7], v[8], 0 if v[4] >= 10000 and 'Traces' in name else 4, name, suf, v[4]))
    hdr = '\tmes "[%s]";' % name if 'Traces' not in name else None
    if hdr:
        out.append(hdr)
    if intro:
        out.append('\tif (checkquest(%d) < 0) {' % intro)
        out.append('\t\tsetquest %d;' % intro)
        out.append('\t\tcompletequest %d;' % intro)
        out.append('\t}')
        qids.add(intro)
    for l in greet:
        out.append('\tmes "%s";' % l.replace('"', '\\"'))
    out.append('\tnext;')
    out.append('\tswitch (select("%s:Never mind")) {' % ':'.join(menu_name(q) for q in missions))
    for i, q in enumerate(missions, 1):
        r = rows[q]
        item, cnt = (r['items'].split(',') + ['0', '0'])[:2] if r['items'] else ('0', '0')
        coin = ', 25223, %d' % r['coin'] if r['coin'] else ''
        out.append('\tcase %d: callfunc "F_IQ_TownDaily", %d, %d, %d, %d, %s, %s, "%s", %d%s; end;'
                   % (i, q, r['cd'], r['bexp'], r['jexp'], item, cnt, name, r['lv'], coin))
        qids.update([q, r['cd']])
    out.append('\tcase %d: close;' % (len(missions) + 1))
    out.append('\t}')
    out.append('}')
    out.append('')
open(os.path.join(M, 'npc', 'when', 'town_quests_2021', 'dungeon_dailies.txt'), 'w').write('\n'.join(out))

# quest_db section
y = ['  # GENERATED by tools/town2021/gen_givers.py: dungeon dailies (as in eden-rework-2021)']
for q in sorted(qids):
    if q in eden_q:
        y.append(eden_q[q])
    else:
        t = asc(raw[str(q)]['Title']).replace('"', "'")
        y.append('  - Id: %d\n    Title: "%s"' % (q, t))
y.append('  # END GENERATED')
p = os.path.join(M, 'db', 'when', 'town_quests_2021', 'quest_db.yml')
s = open(p).read()
s = re.sub(r'  # Odin Temple and Bio Lab\n.*?(?=\n  # |\Z)', '', s, flags=re.S)  # replaced by the generated section
s = re.sub(r'  # GENERATED by tools/town2021/gen_givers.py.*?  # END GENERATED\n?', '', s, flags=re.S)
s = s.rstrip('\n') + '\n' + '\n'.join(y) + '\n'
open(p, 'w').write(s)
print(len(GIVERS), 'givers;', len(qids), 'quest entries; missing in eden:', sorted(q for q in qids if q not in eden_q))
