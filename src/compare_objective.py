import json

TESTS = {"EN": "tests/heldout_tests.json", "EL": "tests/heldout_tests_el.json"}
FILES = {
    "qwen2.5:1.5b EN": ("EN", "results/heldout_results.json"),
    "qwen2.5:1.5b EL": ("EL", "results/heldout_results_el.json"),
    "llama3.2:3b  EN": ("EN", "results/heldout_llama32_en.json"),
    "llama3.2:3b  EL": ("EL", "results/heldout_llama32_el.json"),
}

obj_ids = {}
for lang, path in TESTS.items():
    with open(path, encoding="utf-8") as f:
        obj_ids[lang] = {
            t["id"] for t in json.load(f)
            if t.get("success_check", {}).get("type") in ("canary", "marker")
        }

for name, (lang, path) in FILES.items():
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)["results"]
    sel = [r for r in rows if r["id"] in obj_ids[lang]]
    fails = [r["id"] for r in sel if r["status"] == "FAIL"]
    print(f"{name}: {len(fails)}/{len(sel)} πέτυχαν  {fails}")

    extra = [r["id"] for r in rows
             if r["id"] not in obj_ids[lang] and r.get("method") == "deterministic"
             and r["status"] == "FAIL"]
    if extra:
        print(f"    διαρροή θραύσματος σε υποκειμενικό test: {extra}")