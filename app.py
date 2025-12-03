from flask import Flask, render_template, request
import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


FEED_URLS = [
    "https://techcrunch.com/feed/",
    "http://feeds.bbci.co.uk/news/technology/rss.xml"
]

app = Flask(__name__)



def send_email(to_email, articles):
    sender = EMAIL_USER
    app_password = EMAIL_PASS

    body = ""
    for i, art in enumerate(articles, start=1):
        body += f"{i}. {art['title']}\n"
        body += f"Link: {art['link']}\n"
        body += f"Description: {art['description']}\n\n"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = "Your News Alerts"
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False


def fetch_all_articles():
    all_articles = []

    for url in FEED_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_articles.append({
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "description": entry.get("description", "").strip()
            })

    return all_articles


def filter_articles(articles, keywords):
    result = []
    keywords = [k.lower().strip() for k in keywords]

    for art in articles:
        text = (art["title"] + " " + art["description"]).lower()
        if any(keyword in text for keyword in keywords):
            result.append(art)

    return result


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        keywords = request.form.get("keywords")

        keywords_list = [k.strip() for k in keywords.split(",")]

        all_articles = fetch_all_articles()
        filtered = filter_articles(all_articles, keywords_list)

    # 🚀 SEND THE EMAIL HERE
        send_status = send_email(email, filtered)

        return render_template(
        "index.html",
        email=email,
        keywords=keywords,
        results=filtered,
        sent=send_status
    )


    # ← this was missing
    return render_template("index.html", email=None, keywords=None, results=None)


        

if __name__ == "__main__":
    app.run(debug=True)
