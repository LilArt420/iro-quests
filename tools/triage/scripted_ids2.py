"""Loose scan: every number in a quest-using script file, except lines that
are clearly about items, monsters, skills, effects or coordinates."""
import os, re, json, sys
QC = re.compile(r'\b(setquest|completequest|checkquest|changequest|erasequest|questinfo|isbegin_quest|questprogress|getquest|delquest)\b')
SKIP = re.compile(r'\b(getitem\w*|delitem\w*|countitem\w*|getnameditem|rentitem\w*|getitembound|monster|areamonster|bonus\w*|specialeffect\w*|skilleffect|itemskill|skill|warp|areawarp|movenpc|cutin|emotion|soundeffect|setlook|changelook|sc_start\w*|percentheal|heal|getexp\w*|set Zeny|Zeny|viewpoint|addtimer|initnpctimer|setnpctimer|sleep2?|unitwalk|getmapxy|showevent|getrefine|getequip\w*|equip|autoequip|callshop|npcshop\w*|sellitem|consumeitem|makeitem|setmapflag|instance\w*|getmonsterinfo|killmonster|mobcount|getmobdrops|setunitdata)\b|<ITEM>|<URL>|\^[0-9A-Fa-f]{6}.*\d', re.I)
roots = sys.argv[1:]
ids = {}
for root in roots:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(('.txt', '.conf')): continue
            p = os.path.join(dp, f)
            txt = open(p, encoding='latin-1').read()
            if not QC.search(txt): continue
            rel = os.path.relpath(p, root)
            for line in txt.splitlines():
                s = line.split('//')[0]
                if not s.strip(): continue
                if SKIP.search(s) and not QC.search(s): continue
                if re.match(r'^[\w@-]+,\d+,\d+', s): continue  # npc header
                for n in re.findall(r'(?<![\w.$@\'])(\d{3,6})(?![\w.])', s):
                    ids.setdefault(int(n), set()).add(rel)
json.dump({k: sorted(v) for k, v in ids.items()}, open('scripted_ids_loose.json', 'w'))
print(len(ids))
