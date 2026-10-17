import json
import sys

RESULTS = sys.argv[1] if len(sys.argv) > 1 else "results/test_results.json"
LABELS = sys.argv[2] if len(sys.argv) > 2 else "tests/labels.json"

with open(LABELS, encoding="utf-8") as f:
    labels = json.load(f)
with open(RESULTS, encoding="utf-8") as f:
    data = json.load(f)


def metrics(rows, title):
    tp = fp = fn = tn = 0
    for r in rows:
        truth = labels[r["id"]] == "FAIL"   # θετικό = η επίθεση πέτυχε
        pred = r["status"] == "FAIL"
        if truth and pred:
            tp += 1
        elif pred and not truth:
            fp += 1
        elif truth and not pred:
            fn += 1
        else:
            tn += 1
    n = tp + fp + fn + tn
    if n == 0:
        print(f"{title}: κανένα δείγμα")
        return
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    print(f"{title}  (n={n})")
    print(f"  agreement: {(tp + tn) / n:.0%}   precision: {precision:.0%}   recall: {recall:.0%}")
    print(f"  TP={tp} FP={fp} FN={fn} TN={tn}\n")


scored = [r for r in data["results"]
          if r["id"] in labels and r["status"] in ("PASS", "FAIL")]

metrics(scored, "ΟΛΟΣ ο evaluator")
metrics([r for r in scored if r.get("method") == "llm_judge"], "ΜΟΝΟ ο LLM judge")

print("=== Χωρίς σήμανση (πρόσθεσέ τα στο labels.json) ===")
for r in data["results"]:
    if r["id"] not in labels:
        print(f"\n[{r['id']}] status={r['status']}")
        print("PROMPT:  ", r["prompt"][:150])
        print("RESPONSE:", r["response"][:250])

print("\n=== Διαφωνίες ===")
for r in scored:
    truth = labels[r["id"]]
    if truth != r["status"]:
        print(f"[{r['id']}] εσύ={truth} evaluator={r['status']} -> {r['reasons']}")