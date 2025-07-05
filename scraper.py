import os, re, requests, shutil
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_html(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def save_assets(html, base_url, asset_dir="temp"):
    os.makedirs(asset_dir, exist_ok=True)
    soup = BeautifulSoup(html, "html.parser")
    assets = {
        "css": [link['href'] for link in soup.find_all("link", rel="stylesheet") if link.get("href")],
        "js": [script['src'] for script in soup.find_all("script", src=True)],
        "images": [img['src'] for img in soup.find_all("img", src=True)],
    }

    for typ, urls in assets.items():
        for link in urls:
            try:
                full_url = urljoin(base_url, link)
                filename = os.path.basename(urlparse(full_url).path)
                if not filename:
                    continue
                response = requests.get(full_url, stream=True, timeout=10)
                with open(os.path.join(asset_dir, f"{typ}_{filename}"), 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
            except:
                continue

    return assets

def extract_metadata(html):
    soup = BeautifulSoup(html, 'html.parser')
    return {
        "title": soup.title.string if soup.title else "",
        "description": soup.find("meta", attrs={"name": "description"})['content']
        if soup.find("meta", attrs={"name": "description"}) else ""
    }

def detect_tech(html):
    html_lower = html.lower()
    tech = []
    if "react" in html_lower: tech.append("React")
    if "vue" in html_lower: tech.append("Vue.js")
    if "jquery" in html_lower: tech.append("jQuery")
    if "bootstrap" in html_lower: tech.append("Bootstrap")
    return tech

def extract_emails_and_social(html):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "emails": list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", html))),
        "social_links": list({a['href'] for a in soup.find_all("a", href=True)
                              if any(x in a['href'] for x in ["facebook.com", "twitter.com", "linkedin.com", "instagram.com"])})
    }
