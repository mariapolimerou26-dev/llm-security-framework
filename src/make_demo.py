import json

with open("tests/heldout_tests.json", encoding="utf-8") as f:
    tests = json.load(f)

wanted = {"HO-003", "HO-006", "HO-010"}
demo = [t for t in tests if t["id"] in wanted]

with open("tests/demo_tests.json", "w", encoding="utf-8") as f:
    json.dump(demo, f, indent=4, ensure_ascii=False)

print(f"[+] Written {len(demo)} demo tests: {[t['id'] for t in demo]}")