from flask import Flask, Response
import requests
from datetime import datetime

app = Flask(__name__)

API_URL = "https://api.iranintl.com/news?limit=20"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@app.route("/rss")
def rss():
    try:
        r = requests.get(API_URL, headers=HEADERS, timeout=10)
        data = r.json()

        items = []

        for article in data.get("data", []):
            title = article.get("title", "No title")
            link = "https://www.iranintl.com/" + article.get("slug", "")
            pub = article.get("published_at", datetime.utcnow().isoformat())

            items.append(f"""
                <item>
                    <title>{title}</title>
                    <link>{link}</link>
                    <guid>{link}</guid>
                    <pubDate>{pub}</pubDate>
                </item>
            """)

        rss_feed = f"""
            <rss version="2.0">
                <channel>
                    <title>Iran International – Custom RSS</title>
                    <link>https://www.iranintl.com</link>
                    <description>Unofficial RSS feed generated from IranIntl API</description>
                    {''.join(items)}
                </channel>
            </rss>
        """

        return Response(rss_feed, mimetype="application/rss+xml")

    except Exception as e:
        return f"Error: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
