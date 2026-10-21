import sys, json
sys.path.insert(0, '/Users/arthurmartins/Projects/rathena-ep19/tools/regional_items')
import luadata
F = "/Users/arthurmartins/Documents/Games/Ragnarok Offline/Ragnarok-Portable/Ragnarok/Game (Client)/System/OngoingQuestInfoList_True.lub"
G = luadata.load_any(F, 'latin-1')
print(type(G), list(G.keys())[:10] if isinstance(G, dict) else '')
def conv(v):
    if isinstance(v, dict):
        return {str(k): conv(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [conv(x) for x in v]
    return v
json.dump(conv(G), open('quests_client.json', 'w'), indent=1, ensure_ascii=False)
