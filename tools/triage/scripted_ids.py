import os, re, json, sys
QC = r'(?:setquest|completequest|checkquest|changequest|erasequest|questinfo|isbegin_quest|questprogress|getquest|delquest)'
CMD = re.compile(r'\b' + QC + r'\b')
ARG = re.compile(r'\b' + QC + r'\s*\(?\s*([.$@'"'"']*\w+)')
roots = sys.argv[1:]
ids = {}
def add(n, rel): ids.setdefault(n, set()).add(rel)
for root in roots:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(('.txt', '.conf')): continue
            p = os.path.join(dp, f)
            txt = open(p, encoding='latin-1').read()
            if not CMD.search(txt): continue
            rel = os.path.relpath(p, root)
            lines = [l.split('//')[0] for l in txt.splitlines()]
            vars_ = set()
            for s in lines:
                if CMD.search(s):
                    for n in re.findall(r'(?<![\w.$@\'])(\d{3,6})(?![\w.])', s): add(int(n), rel)
                    for v in ARG.findall(s):
                        if not v.isdigit(): vars_.add(v)
                    # also callfunc args e.g. callsub L_Quest, 1234
            # callfunc / callsub with quest-ish names and any var used in quest commands
            vn = {v for v in vars_}
            for s in lines:
                for v in vn:
                    if re.search(r'(setarray\s+' + re.escape(v) + r'\b|' + re.escape(v) + r'\s*(\[[^\]]*\])?\s*=[^=])', s):
                        for n in re.findall(r'(?<![\w.$@\'])(\d{3,6})(?![\w.])', s): add(int(n), rel)
                # getarg-based functions: lines calling subs/functions that set quests
            for s in lines:
                if re.search(r'callsub|callfunc|\bF_\w+|\bS_\w+', s) and re.search(r'[Qq]uest', s):
                    for n in re.findall(r'(?<![\w.$@\'])(\d{4,6})(?![\w.])', s): add(int(n), rel)
json.dump({k: sorted(v) for k, v in ids.items()}, open('scripted_ids.json', 'w'))
print(len(ids))
