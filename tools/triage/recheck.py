"""Re-check the triage: which missing quests are live on iRO and not already in the game.
In: keys.json (keys.py + signals.py + server text), wiki_hits.json {key: [page,...]}, wiki_pages.json {page: section}
Out: recheck.json, prints a summary."""
import json, re, collections
k = json.load(open('keys.json'))
hits = json.load(open('wiki_hits.json'))
sec = json.load(open('wiki_pages.json'))
EVENT_SEC = re.compile(r'^(19|20)\d\d$|Obsolete')
def wiki(term):
    ps = hits.get(term.lower(), [])
    perm = [p for p in ps if not EVENT_SEC.search(sec.get(p, ''))]
    ev = [p for p in ps if EVENT_SEC.search(sec.get(p, ''))]
    return perm, ev
chains = collections.OrderedDict()
for q in sorted(k, key=lambda q: q['id']):
    chains.setdefault((q['pack'], q['key'].lower()), []).append(q)
res = []
for (pack, key), qs in chains.items():
    perm, ev = wiki(key) if len(key) >= 8 and len(key.split()) >= 2 else ([], [])
    gp, ge = [], []
    for q in qs:
        for g in q['givers']:
            a, b = wiki(g[0]); gp += a; ge += b
    gp = sorted(set(gp)); ge = sorted(set(ge))
    in_game = any(q['srv_text'] or q['srv_npc'] for q in qs)
    iro_npc = any(q['iro_npc'] for q in qs)
    if pack.startswith('iRO Gramps'):
        verdict = 'system: Gramps'
    elif perm:
        verdict = 'in game already' if in_game else 'GAP (iROWiki)'
    elif ev and not perm:
        verdict = 'event (iROWiki)'
    elif gp and len(gp) <= 6:
        verdict = 'in game already' if in_game else 'GAP (giver on iROWiki)'
    elif iro_npc:
        verdict = 'in game already' if in_game else 'maybe (giver in iRO NPC table)'
    else:
        verdict = 'in game already' if in_game else 'not on iRO'
    areas = collections.Counter(q['area'] for q in qs).most_common(1)[0][0]
    res.append(dict(pack=pack, key=key, ids=[q['id'] for q in qs], area=areas, verdict=verdict, wiki=perm[:3] or gp[:3], wiki_ev=ev[:2],
                    srv=[q['srv_text'] for q in qs if q['srv_text']][:1] + [e for q in qs for e in q['ev'] if e.startswith('srv')][:1],
                    title=qs[0]['title']))
json.dump(res, open('recheck.json', 'w'), indent=0)
c = collections.Counter(r['verdict'] for r in res); ci = collections.Counter()
for r in res: ci[r['verdict']] += len(r['ids'])
for v in c: print(f'{v:32} chains {c[v]:4}  entries {ci[v]:5}')
