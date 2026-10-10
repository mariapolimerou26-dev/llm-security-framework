import json
from datetime import datetime
from pathlib import Path
from collections import Counter
import requests

from evaluator import evaluate_response


TEST_FILE = Path("tests/security_tests.json")
RESULT_FILE = Path("results/test_results.json")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"


def load_tests():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_llm_response(prompt):
    """
    Sends the prompt to the local Ollama instance running Qwen 2.5
    and returns the model's actual response.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"[Error: Ollama returned status {response.status_code}]"
    except Exception as e:
        return f"[Error connecting to Ollama: {str(e)}]"


def run_test(test):
    print(f"[+] Running test: {test['id']}")
    print(f"    Category: {test['category']}")
    print(f"    Prompt: {test['prompt']}")

    # Παίρνουμε την πραγματική απάντηση από το τοπικό LLM
    response = get_llm_response(test['prompt'])

    print(f"    Response: {response}")

    evaluation = evaluate_response(test, response)

    result = {
        "id": test["id"],
        "category": test["category"],
        "prompt": test["prompt"],
        "response": response,
        "status": evaluation["status"],
        "severity": evaluation["severity"],
        "detected_leakage": evaluation["detected_leakage"],
        "detected_override": evaluation["detected_override"],
        "detected_refusal": evaluation["detected_refusal"],
        "timestamp": datetime.now().isoformat(),
    }

    print(f"    Status: {result['status']}")
    print()

    return result


def generate_summary(results):
    total = len(results)
    passed = sum(1 for result in results if result["status"] == "PASS")
    failed = sum(1 for result in results if result["status"] == "FAIL")

    failure_rate = (failed / total * 100) if total > 0 else 0

    failed_categories = Counter(
        result["category"]
        for result in results
        if result["status"] == "FAIL"
    )

    severity_counts = Counter(
        result["severity"]
        for result in results
        if result["status"] == "FAIL"
    )

    summary = {
        "total_tests": total,
        "passed": passed,
        "failed": failed,
        "failure_rate_percent": round(failure_rate, 2),
        "failures_by_category": dict(failed_categories),
        "failures_by_severity": dict(severity_counts),
    }

    return summary


def save_results(results, summary):
    output = {
        "summary": summary,
        "results": results,
    }

    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, ensure_ascii=False)

    print(f"[+] Results saved to: {RESULT_FILE}")


def main():
    tests = load_tests()

    print(f"[*] Loaded {len(tests)} security tests")
    print(f"[*] Connected to Local LLM ({MODEL_NAME}) via Ollama")
    print()

    results = []

    for test in tests:
        result = run_test(test)
        results.append(result)

    summary = generate_summary(results)

    print("=== Security Summary ===")
    print(f"Total tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Failure rate: {summary['failure_rate_percent']}%")
    print()

    print("Failures by category:")
    if summary["failures_by_category"]:
        for category, count in summary["failures_by_category"].items():
            print(f"- {category}: {count}")
    else:
        print("- None")

    print()

    print("Failures by severity:")
    if summary["failures_by_severity"]:
        for severity, count in summary["failures_by_severity"].items():
            print(f"- {severity}: {count}")
    else:
        print("- None")

    print()

    save_results(results, summary)

    print()
    print(f"[+] Completed {len(tests)} tests with real LLM")


if __name__ == "__main__":
    main()
