@echo off
call .venv\Scripts\activate

echo.
echo === 1. Unit tests του evaluator ===
pytest

echo.
echo === 2. Αξιοπιστία του judge (held-out, n=20) ===
python src\judge_eval.py results\heldout_results.json tests\labels_heldout.json

echo.
echo === 3. HTML report ===
start results\security_report.html

echo.
echo === Για ζωντανό τρέξιμο (χρειάζεται Ollama) ===
echo python src\runner.py tests\heldout_tests.json results\demo.json
pause