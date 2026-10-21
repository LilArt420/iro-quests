"""Overlook Water Dungeon: iRO's VIP copy of the Byalan dungeon (iz_dun00t-iz_dun04t).

Writes, into MODDIR:
  db/when/overlook_water_dungeon/mob_db.yml     the 15 Aged monsters (iRO ids 2501-2515)
  db/when/overlook_water_dungeon/mob_avail.yml  each one drawn with its Byalan monster's sprite
  npc/when/overlook_water_dungeon/overlook_spawns.txt

Usage: python3 gen_overlook.py WORKDIR MODDIR
  WORKDIR/byalan_base.json  the server's mob_db entries of the 15 Byalan monsters
  WORKDIR/item_names.json   item name (lower case) -> AegisName

Stats, EXP, drops and spawns are the iRO database's (db.irowiki.org monster-info 2501-2515 and
map-info iz_dun00t-iz_dun04t, read from the Internet Archive). Level, AGI, INT, DEX, LUK,
range, speed, AI and motions are the Byalan monster's, which the iRO figures match; ATK uses
the same conversion as the World Sync monsters: Attack = middle of the ATK range - STR - level.
"""
import sys, os, re, json

W, M = sys.argv[1], sys.argv[2]
base = json.load(open(os.path.join(W, 'byalan_base.json')))
items = json.load(open(os.path.join(W, 'item_names.json')))

# id, iRO name, Byalan base, HP, DEF, MDEF, ATK min, ATK max, Base EXP, Job EXP, element level, drops
AGED = [
 (2501, 'Aged Cornutus', 'CORNUTUS', 7250, 55, 36, 143, 174, 1107, 1242, 1,
  'Crystal Blue 0.91% Conch 100.00% Scell 16.00% Rough Elunium 1.07% Shield [1] 0.11% Solid Shell 20.00% Blue Gemstone 2.00% Cornutus Card 0.03%'),
 (2502, 'Aged Deviace', 'DEVIACE', 15675, 66, 21, 245, 309, 1974, 2220, 4,
  'Mystic Frozen 0.51% Ancient Tooth 100.00% Ancient Lips 20.00% Aerial 0.05% Detrimindexta 4.00% Katar of Frozen Icicle 0.07% Rough Oridecon 3.23% Deviace Card 0.03%'),
 (2503, 'Aged Hydra', 'HYDRA', 4270, 26, 42, 72, 86, 699, 789, 2,
  'Emveretarcon 0.51% Tentacle 100.00% Sticky Mucus 30.00% Detrimindexta 0.41% Panacea 0.11% Meat 14.00% Hydra Card 0.03%'),
 (2504, 'Aged Kukre', 'KUKRE', 5555, 43, 30, 119, 145, 945, 1062, 1,
  "Crystal Blue 0.61% Insect Peeling 100.00% Garlet 8.00% Monster's Feed 10.00% Red Herb 13.00% Insect Feeler 9.00% Earthworm the Dude 0.41% Kukre Card 0.03%"),
 (2505, 'Aged Marc', 'MARC', 12610, 72, 31, 216, 271, 1575, 1770, 2,
  'Mystic Frozen 0.37% Gill 100.00% Rough Oridecon 1.91% Fin 20.00% Aquamarine 0.21% Blue Gemstone 4.00% White Herb 14.00% Marc Card 0.03%'),
 (2506, 'Aged Marina', 'MARINA', 6045, 26, 25, 124, 153, 1020, 1143, 2,
  'Single Cell 100.00% Sticky Mucus 30.00% Crystal Blue 0.91% Mystic Frozen 0.05% Blue Gemstone 4.00% Deadly Noxious Herb 0.41% Marina Card 0.03%'),
 (2507, 'Aged Marine Sphere', 'MARINE_SPHERE', 9620, 53, 36, 61, 62, 1338, 1509, 2,
  'Tendon 100.00% Detonator 50.00% Chain [3] 0.21% Aquamarine 0.21% Blue Gemstone 3.00% Transparent Head Protector 0.21% Marine Sphere Card 0.03%'),
 (2508, 'Aged Marse', 'MARSE', 7280, 49, 23, 148, 182, 1167, 1314, 2,
  'Squid Ink 100.00% Tentacle 60.00% Blue Gemstone 4.00% Aquamarine 0.21% Mystic Frozen 0.25% Necklace of Wisdom 0.11% Grape 6.00% Marse Card 0.03%'),
 (2509, 'Aged Merman', 'MERMAN', 14700, 81, 10, 205, 255, 1848, 2076, 3,
  'Ancient Lips 26.00% Full Plate [1] 0.05% Lemon 8.00% Aquamarine 0.81% Mystic Frozen 0.71% Trident [2] 0.07% Rough Oridecon 4.07% Merman Card 0.03%'),
 (2510, 'Aged Obeaune', 'OBEAUNE', 10790, 62, 34, 188, 229, 1428, 1602, 2,
  "Mystic Frozen 0.27% Mermaid's Heart 100.00% Fin Helm 0.03% Saint's Robe [1] 0.21% Aquamarine 0.21% Fin 10.00% Witherless Rose 0.61% Obeaune Card 0.03%"),
 (2511, 'Aged Phen', 'PHEN', 9815, 57, 14, 183, 222, 1338, 1509, 2,
  'Fish Tail 100.00% Sharp Scale 40.00% Aquamarine 0.11% Meat 20.00% Fin 10.00% Rough Oridecon 0.51% Phen Card 0.03%'),
 (2512, 'Aged Plankton', 'PLANKTON', 6160, 36, 36, 123, 153, 1002, 1125, 3,
  'Single Cell 100.00% Garlet 6.00% Sticky Mucus 14.00% Alcohol 0.09% Empty Bottle 20.00% Dew Laden Moss 0.41% Concentration Potion 1.00% Plankton Card 0.03%'),
 (2513, 'Aged Strouf', 'STROUF', 15260, 87, 27, 239, 304, 1878, 2115, 3,
  'Fin 100.00% Rough Oridecon 2.31% Chain Mail [1] 0.05% Trident [3] 0.05% Feather 60.00% Aquamarine 0.41% Gill 30.00% Strouf Card 0.03%'),
 (2514, 'Aged Swordfish', 'SWORD_FISH', 13000, 68, 16, 226, 285, 1575, 1770, 2,
  'Mystic Frozen 0.21% Sharp Scale 100.00% Rough Oridecon 0.67% Unicorn Horn 0.05% Rough Elunium 1.00% Katana [4] 0.51% Gill 12.00% Swordfish Card 0.03%'),
 (2515, 'Aged Vadon', 'VADON', 6260, 70, 27, 142, 173, 1026, 1158, 1,
  'Crystal Blue 0.81% Nipper 100.00% Garlet 60.00% Padded Armor [1] 0.11% Solid Shell 2.00% Rough Elunium 0.81% Blue Gemstone 1.00% Vadon Card 0.03%'),
]
# map: [(id, count, respawn ms)]  (iRO database map-info)
SPAWNS = {
 'iz_dun00t': [(2503, 15, 0), (2512, 65, 0), (2504, 15, 0), (2506, 45, 0), (2515, 15, 0)],
 'iz_dun01t': [(2503, 30, 0), (2512, 10, 0), (2504, 50, 0), (2506, 15, 0), (2515, 60, 0), (2501, 15, 300000)],
 'iz_dun02t': [(2503, 40, 0), (2508, 40, 0), (2501, 60, 0), (2510, 40, 0), (2509, 1, 1800000)],
 'iz_dun03t': [(2503, 10, 0), (2507, 20, 0), (2511, 45, 0), (2505, 40, 0), (2514, 40, 0), (2509, 3, 1800000)],
 'iz_dun04t': [(2503, 18, 300000), (2507, 10, 0), (2514, 10, 0), (2502, 3, 0), (2509, 40, 0), (2513, 50, 600000)],
}
ALIAS = {'chain [3]': 'Chain_', 'shield [1]': 'Shield_', 'full plate [1]': 'Plate_Armor_', 'trident [2]': 'Trident',
         'trident [3]': 'Trident_', "saint's robe [1]": 'Saint_Robe_', 'chain mail [1]': 'Chain_Mail_',
         'padded armor [1]': 'Padded_Armor_', 'katana [4]': 'Katana__', 'mystic frozen': 'Mistic_Frozen', 'insect peeling': 'Worm_Peelings', "mermaid's heart": 'Heart_Of_Mermaid',
         'earthworm the dude': 'Earthworm_The_Dude', 'transparent head protector': 'Transparent_Headgear'}


def aegis_of(name):
    n = name.lower()
    if n in ALIAS:
        return ALIAS[n]
    if n in items:
        return items[n]
    n2 = re.sub(r'\s*\[\d\]$', '', n)
    return items.get(n2)


drops_out, missing = {}, []
for mid, name, b, *_rest, dtext in AGED:
    ds = []
    for nm, pct in re.findall(r"(.+?) (\d+\.\d+)%\s*", dtext):
        a = aegis_of(nm.strip())
        if not a:
            missing.append((name, nm)); continue
        ds.append((a, max(1, round(float(pct) * 100)), nm.strip().endswith('Card')))
    drops_out[mid] = ds
if missing:
    print('UNMAPPED DROPS:', missing)

out = ['# iRO Quests: the Overlook Water Dungeon\'s Aged monsters (iRO ids 2501-2515).',
       '# Generated by tools/overlook/gen_overlook.py from the iRO database; edit the generator.',
       'Header:', '  Type: MOB_DB', '  Version: 5', '', 'Body:']
avail = ['Header:', '  Type: MOB_AVAIL_DB', '  Version: 1', '', 'Body:']
for mid, name, b, hp, df, mdf, amin, amax, bexp, jexp, elv, _d in AGED:
    s = base[b]
    aeg = 'AGED_' + b
    atk = max(1, round((amin + amax) / 2) - s.get('Str', 0) - s['Level'])
    out += ['  - Id: %d' % mid, '    AegisName: %s' % aeg, '    Name: %s' % name, '    Level: %d' % s['Level'],
            '    Hp: %d' % hp, '    BaseExp: %d' % bexp, '    JobExp: %d' % jexp,
            '    Attack: %d' % atk, '    Attack2: %d' % s.get('Attack2', 0), '    Defense: %d' % df, '    MagicDefense: %d' % mdf]
    for k in ('Str', 'Agi', 'Vit', 'Int', 'Dex', 'Luk', 'AttackRange', 'SkillRange', 'ChaseRange'):
        if k in s:
            out.append('    %s: %s' % (k, s[k]))
    for k in ('Size', 'Race'):
        if k in s:
            out.append('    %s: %s' % (k, s[k]))
    out += ['    Element: %s' % s.get('Element', 'Water'), '    ElementLevel: %d' % elv]
    for k in ('WalkSpeed', 'AttackDelay', 'AttackMotion', 'DamageMotion', 'Ai'):
        if k in s:
            out.append('    %s: %s' % (k, s[k] if k != 'Ai' else '"%02d"' % int(s[k])))
    if s.get('Modes'):
        out.append('    Modes:')
        out += ['      %s: true' % m for m in s['Modes']]
    out.append('    Drops:')
    for a, r, card in drops_out[mid]:
        out += ['      - Item: %s' % a, '        Rate: %d' % r]
        if card:
            out.append('        StealProtected: true')
    avail += ['  - Mob: %s' % aeg, '    Sprite: %s' % b]

dbdir = os.path.join(M, 'db', 'when', 'overlook_water_dungeon')
os.makedirs(dbdir, exist_ok=True)
open(os.path.join(dbdir, 'mob_db.yml'), 'w').write('\n'.join(out) + '\n')
open(os.path.join(dbdir, 'mob_avail.yml'), 'w').write('\n'.join(avail) + '\n')

S = ['//===== Ragnarok Offline mod: iRO Quests =====================',
     '//= Overlook Water Dungeon: Aged monster spawns (iRO database map-info).',
     '//= Generated by tools/overlook/gen_overlook.py; edit the generator.',
     '//============================================================', '']
names = {a[0]: a[1] for a in AGED}
for m, rows in SPAWNS.items():
    for mid, n, delay in rows:
        S.append('%s,0,0\tmonster\t%s\t%d,%d%s' % (m, names[mid], mid, n, ',%d,0' % delay if delay else ''))
    S.append('')
npcdir = os.path.join(M, 'npc', 'when', 'overlook_water_dungeon')
os.makedirs(npcdir, exist_ok=True)
open(os.path.join(npcdir, 'overlook_spawns.txt'), 'w').write('\n'.join(S))
print('monsters', len(AGED), 'drops', sum(len(v) for v in drops_out.values()))
