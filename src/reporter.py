import json
from pathlib import Path

RESULT_FILE = Path("results/test_results.json")
HTML_FILE = Path("results/security_report.html")

def load_results():
    if not RESULT_FILE.exists():
        print(f"[!] Result file not found: {RESULT_FILE}")
        return None
    with open(RESULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_html_report(data):
    summary = data["summary"]
    results = data["results"]

    html_content = f"""<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>Local LLM Security Evaluation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }}
        .container {{ max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; }}
        .summary-box {{ display: flex; justify-content: space-around; background: #eef2f7; padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
        .summary-item {{ text-align: center; }}
        .summary-item h3 {{ margin: 0; font-size: 24px; color: #2980b9; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; font-size: 14px; vertical-align: top; }}
        th {{ background-color: #f8f9fa; }}
        .badge-pass {{ background-color: #2ecc71; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .badge-fail {{ background-color: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        .response-box {{ background: #f8f9fa; padding: 8px; border-left: 3px solid #ccc; font-family: monospace; white-space: pre-wrap; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Local LLM Security Evaluation Report</h1>
        <div class="summary-box">
            <div class="summary-item"><h3>{summary['total_tests']}</h3><p>Συνολικά Τεστ</p></div>
            <div class="summary-item"><h3 style="color: #27ae60;">{summary['passed']}</h3><p>Επιτυχίες (PASS)</p></div>
            <div class="summary-item"><h3 style="color: #c0392b;">{summary['failed']}</h3><p>Αποτυχίες (FAIL)</p></div>
            <div class="summary-item"><h3 style="color: #d35400;">{summary['failure_rate_percent']}%</h3><p>Ποσοστό Αποτυχίας</p></div>
        </div>
        <h2>Αναλυτικά Αποτελέσματα Τεστ</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Κατηγορία</th>
                    <th>Status</th>
                    <th>Σοβαρότητα</th>
                    <th>Prompt & Απάντηση LLM</th>
                </tr>
            </thead>
            <tbody>
    """

    for r in results:
        status_badge = '<span class="badge-pass">PASS</span>' if r['status'] == 'PASS' else '<span class="badge-fail">FAIL</span>'
        html_content += f"""
                <tr>
                    <td><strong>{r['id']}</strong></td>
                    <td>{r['category']}</td>
                    <td>{status_badge}</td>
                    <td>{r.get('severity', 'N/A')}</td>
                    <td>
                        <strong>Prompt:</strong> {r['prompt']}<br>
                        <strong>Response:</strong>
                        <div class="response-box">{r['response']}</div>
                    </td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
    """

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] HTML Report generated successfully: {HTML_FILE}")

if __name__ == "__main__":
    data = load_results()
    if data:
        generate_html_report(data)