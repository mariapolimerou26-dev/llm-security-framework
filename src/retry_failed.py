import json
from runner import load_tests, run_test, generate_summary, RESULT_FILE

tests = {t["id"]: t for t in load_tests()}

with open(RESULT_FILE, encoding="utf-8") as f:
    data = json.load(f)

for i, r in enumerate(data["results"]):
    if r["status"] in ("ERROR", "UNJUDGED"):
        print(f"[*] Retry {r['id']}")
        data["results"][i] = run_test(tests[r["id"]])

data["summary"] = generate_summary(data["results"])

with open(RESULT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("[+] Updated", RESULT_FILE)
print(data["summary"])