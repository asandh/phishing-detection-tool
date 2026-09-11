from flask import Flask, request

app = Flask(__name__)

def analyze_url(url):
    score = 0
    warnings = []

    suspicious_words = ["login", "verify", "account", "update", "secure", "bank", "password", "confirm"]

    if not url.startswith("https://"):
        score += 25
        warnings.append("URL does not use HTTPS")

    if len(url) > 75:
        score += 20
        warnings.append("URL is unusually long")

    if "@" in url:
        score += 20
        warnings.append("URL contains @ symbol")

    if "-" in url:
        score += 10
        warnings.append("URL contains hyphens, which are common in fake domains")

    for word in suspicious_words:
        if word in url.lower():
            score += 10
            warnings.append(f"Suspicious keyword found: {word}")

    if score >= 60:
        risk = "High Risk"
    elif score >= 30:
        risk = "Suspicious"
    else:
        risk = "Low Risk"

    return score, risk, warnings


@app.route("/", methods=["GET", "POST"])
def home():
    result_html = ""

    if request.method == "POST":
        url = request.form["url"]
        score, risk, warnings = analyze_url(url)

        warning_items = ""
        for warning in warnings:
            warning_items += f"<li>{warning}</li>"

        result_html = f"""
        <div class="result">
            <h2>Analysis Result</h2>
            <p><strong>URL:</strong> {url}</p>
            <p><strong>Risk Level:</strong> {risk}</p>
            <p><strong>Risk Score:</strong> {score}/100</p>
            <h3>Warnings:</h3>
            <ul>{warning_items if warning_items else "<li>No major warnings detected</li>"}</ul>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Phishing Detection Tool</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                margin: 0;
                padding: 40px;
            }}

            .container {{
                max-width: 800px;
                margin: auto;
                background: #1e293b;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }}

            h1 {{
                text-align: center;
                margin-bottom: 10px;
            }}

            .subtitle {{
                text-align: center;
                color: #94a3b8;
                margin-bottom: 30px;
            }}

            input {{
                width: 100%;
                padding: 14px;
                border-radius: 10px;
                border: none;
                margin-bottom: 15px;
                font-size: 16px;
            }}

            button {{
                width: 100%;
                padding: 14px;
                background: #38bdf8;
                color: #0f172a;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
            }}

            .result {{
                margin-top: 30px;
                background: #020617;
                padding: 20px;
                border-radius: 12px;
            }}

            li {{
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Phishing Detection Tool</h1>
            <p class="subtitle">Analyze URLs for suspicious phishing indicators</p>

            <form method="POST">
                <input type="text" name="url" placeholder="Enter a URL to scan..." required>
                <button type="submit">Analyze URL</button>
            </form>

            {result_html}
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5001)