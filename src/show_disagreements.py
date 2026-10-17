import json
import sys

RESULTS = sys.argv[1] if len(sys.argv) > 1 else "results/test_results.json"
LABELS = sys.argv[2] if len(sys.argv) > 2 else "tests/labels.json"

with open(LABELS, encoding="utf-8") as f:
    labels = json.load(f)
with open(RESULTS, encoding="utf-8") as f:
    data = json.load(f)

for r in data["results"]:
    if r["id"] in labels and r["status"] in ("PASS", "FAIL") and labels[r["id"]] != r["status"]:
        print("\n" + "=" * 60)
        print(f"[{r['id']}] ({r['category']}) εσύ={labels[r['id']]}  evaluator={r['status']}  ({r['method']})")
        print("PROMPT:  ", r["prompt"])
        print("RESPONSE:", r["response"])
        print("REASONS: ", r["reasons"])