import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os


# Load .env file
load_dotenv()


# Get the secret codes from .env
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# RSS Feeds used for this project
FEED_URLS = [
    "https://techcrunch.com/feed/",
    "http://feeds.bbci.co.uk/news/technology/rss.xml"
]

# sends the email
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
    msg["Subject"] = "Your Daily Dose of News!"
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



# download the rss fiels, extract the article data, return a list
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


# filters the articles according to the user's keyword
def filter_articles(articles, keywords):
    result = []
    keywords = [k.lower().strip() for k in keywords]

    for art in articles:
        text = (art["title"] + " " + art["description"]).lower()
        if any(keyword in text for keyword in keywords):
            result.append(art)

    return result