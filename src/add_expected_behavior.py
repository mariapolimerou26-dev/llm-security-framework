import json
from pathlib import Path


TEST_FILE = Path("tests/security_tests.json")


def main():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        tests = json.load(file)

    for test in tests:
        test["expected_behavior"] = "refuse"

    with open(TEST_FILE, "w", encoding="utf-8") as file:
        json.dump(
            tests,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"[+] Updated {len(tests)} tests")
    print("[+] Added expected_behavior='refuse'")


if __name__ == "__main__":
    main()