from flask import Flask, render_template, request, send_file
from scraper import fetch_html, save_assets, extract_metadata, detect_tech, extract_emails_and_social
import os, shutil, zipfile

app = Flask(__name__)
HTML_FILE = "temp/scraped_page.html"
ZIP_FILE = "temp/site_package.zip"

@app.route("/", methods=["GET", "POST"])
def index():
    result = {}
    error = None

    if request.method == "POST":
        url = request.form["url"]
        mode = request.form["mode"]
        result["mode"] = mode
        html = fetch_html(url)

        if html.startswith("Error:"):
            error = html
        else:
            os.makedirs("temp", exist_ok=True)
            with open(HTML_FILE, "w", encoding="utf-8") as f:
                f.write(html)
            result["url"] = url

            if mode == "developer":
                assets = save_assets(html, url)
                result["html"] = html[:5000] + "..." if len(html) > 5000 else html
                result["assets"] = assets
                with zipfile.ZipFile(ZIP_FILE, 'w') as zf:
                    zf.write(HTML_FILE)
                    for filename in os.listdir("temp"):
                        if filename != "site_package.zip":
                            zf.write(os.path.join("temp", filename), arcname=filename)

            elif mode == "full":
                result["html"] = html[:5000] + "..." if len(html) > 5000 else html
                result["meta"] = extract_metadata(html)
                result["tech"] = detect_tech(html)
                result["contacts"] = extract_emails_and_social(html)

    return render_template("index.html", result=result, error=error)

@app.route("/download/html")
def download_html():
    return send_file(HTML_FILE, as_attachment=True) if os.path.exists(HTML_FILE) else "No HTML file."

@app.route("/download/zip")
def download_zip():
    return send_file(ZIP_FILE, as_attachment=True) if os.path.exists(ZIP_FILE) else "No ZIP file."
