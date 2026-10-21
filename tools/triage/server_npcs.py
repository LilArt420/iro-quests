import os, re, json, sys
H = re.compile(r'^([\w@-]+),(\d+),(\d+),\d+\t(script|shop|cashshop|itemshop|pointshop|marketshop|trader|duplicate\([^)]*\))\t([^\t]+)\t', re.M)
out = []
for root in sys.argv[1:]:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith('.txt'): continue
            p = os.path.join(dp, f)
            for m in H.finditer(open(p, encoding='latin-1').read()):
                name = m.group(5)
                disp = name.split('::')[0].split('#')[0].strip()
                out.append([m.group(1), int(m.group(2)), int(m.group(3)), disp, name, os.path.relpath(p, root)])
json.dump(out, open('server_npcs.json', 'w'))
print(len(out))
