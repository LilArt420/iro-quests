import json, collections, sys
out = json.load(open('triage.json'))
chains = []
for r in out:
    c = chains[-1] if chains else None
    if c and r['id'] - c['ids'][-1] <= 3 and (r['area'] == c['area'] or r['area'] == '?' or c['area'] == '?'):
        c['ids'].append(r['id']); c['rows'].append(r)
        if c['area'] == '?': c['area'] = r['area']
    else:
        chains.append(dict(ids=[r['id']], rows=[r], area=r['area']))
for c in chains:
    k = collections.Counter(r['kind'] for r in c['rows'])
    c['kinds'] = dict(k)
    c['titles'] = list(dict.fromkeys(r['title'] for r in c['rows'] if r['kind'] not in ('hidden', 'cooldown')))
json.dump([{k: v for k, v in c.items() if k != 'rows'} for c in chains], open('chains.json', 'w'), ensure_ascii=False)
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for c in chains:
    if lo <= c['ids'][0] < hi:
        print(f"{c['ids'][0]}-{c['ids'][-1]} [{c['area']}] {c['kinds']} :: " + ' | '.join(t[:40] for t in c['titles'][:5]))
