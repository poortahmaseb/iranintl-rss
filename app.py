from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

URL = "https://www.iranintl.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

@app.route("/rss")
def rss():
    try:
        r = requests.get(URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        items = []

        for article in soup.select("a[href*='/202']")[:15]:
            title = article.get_text(strip=True)
            link = "https://www.iranintl.com" + article.get("href")

            items.append(f"""
                <item>
                    <title>{title}</title>
                    <link>{link}</link>
                    <guid>{link}</guid>
                    <pubDate>{datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}</pubDate>
                </item>
            """)

        rss_feed = f"""
            <rss version="2.0">
                <channel>
                    <title>Iran International – Custom RSS</title>
                    <link>{URL}</link>
                    <description>Unofficial RSS feed generated for IranIntl</description>
                    {''.join(items)}
                </channel>
            </rss>
        """

        return Response(rss_feed, mimetype="application/rss+xml")

    except Exception as e:
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
