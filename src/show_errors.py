import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)

for r in data["results"]:
    if r["status"] in ("ERROR", "UNJUDGED"):
        print(f"[{r['id']}] {r['status']}")
        print("  error:  ", r.get("error", ""))
        print("  reasons:", r.get("reasons", ""))