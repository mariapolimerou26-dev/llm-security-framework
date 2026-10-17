import json
from judge import judge_response, JudgeError

with open("results/run1_backup.json", encoding="utf-8") as f:
    data = json.load(f)

for r in data["results"]:
    if r.get("method") != "llm_judge":
        continue
    try:
        v = judge_response(r, r["response"])
        r["status"] = v["status"]
        r["reasons"] = [f"judge: {v['reason']}"]
    except JudgeError as e:
        r["status"] = "UNJUDGED"
        r["reasons"] = [f"judge_error: {e}"]

with open("results/rejudged.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("[+] Saved results/rejudged.json")