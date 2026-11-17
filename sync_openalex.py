import json
import requests
from datetime import datetime, timezone

members_path = 'research/data/members.json'
meta_path    = 'research/data/sync_meta.json'

with open(members_path) as f:
    members = json.load(f)

for m in members:
    if not m.get('openalex_id'):
        continue
    try:
        url = f"https://api.openalex.org/authors/{m['openalex_id']}"
        r = requests.get(url, headers={'User-Agent': 'SLIIT-KandyUNI-sync/1.0'}, timeout=15)
        if r.status_code == 200:
            d = r.json()
            m['works_count']    = d.get('works_count', 0)
            m['cited_by_count'] = d.get('cited_by_count', 0)
            m['h_index']        = d.get('summary_stats', {}).get('h_index')
            m['last_synced']    = datetime.now(timezone.utc).isoformat()
            print(f"Synced {m['name']}: {m['works_count']} works")
    except Exception as e:
        print(f"Error syncing {m['name']}: {e}")

with open(members_path, 'w') as f:
    json.dump(members, f, indent=2)

meta = {
    'last_sync': datetime.now(timezone.utc).isoformat(),
    'status': 'success'
}
with open(meta_path, 'w') as f:
    json.dump(meta, f, indent=2)

print('Sync complete')
