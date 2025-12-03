import feedparser
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


FEED_URL = [
    "https://techcrunch.com/feed/",
    "http://feeds.bbci.co.uk/news/technology/rss.xml"
    ]



def normalize_entry(entry):
    title = entry.get("title", "No title").strip()
    link = entry.get("link", "").strip()
    description = entry.get("description", "").strip() if entry.get("description") else ""
    published = entry.get("published") or entry.get("pubDate") or None


    return{
        "title": title,
        "link": link,
        "description": description,
        "published": published
    }


user_email = input("Enter your email address: ").strip()
keywords_input = input("Enter keywords separated by commas: ")
keywords = [k.strip() for k in keywords_input.split(",")]





all_articles = []


for url in FEED_URL:
    try:
        # Fetch the feed content with a timeout and User-Agent
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()  # raise error if the response is bad

        # Parse the feed content
        feed = feedparser.parse(response.content)
        print(f"\nFetching feed: {feed.feed.get('title')}")

        # Normalize articles
        articles = [normalize_entry(entry) for entry in feed.entries]
        all_articles.extend(articles)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")

print(f"\nTotal articles from all feeds: {len(all_articles)}")





def filter_articles(articles, keywords):
    """
    Returns a list of articles where the title or description
    contains any of the keywords (case-insensitive).
    """
    filtered = []  # This will store the matching articles

    for article in articles:
        title = article['title'].lower()        # convert title to lowercase
        description = article['description'].lower()  # convert description to lowercase
        # If any keyword is in title or description, keep this article
        if any(keyword.lower() in title or keyword.lower() in description for keyword in keywords):
            filtered.append(article)
    return filtered




filtered_articles = filter_articles(all_articles, keywords)

print(f"\nTotal articles after filtering: {len(filtered_articles)}")

body = ""
for i, article in enumerate(filtered_articles, start=1):
    body += f"{i}. {article['title']}\n"
    body += f"Link: {article['link']}\n"
    body += f"Description: {article['description']}\n\n"

msg = MIMEMultipart()
msg['From'] = "bethelhemdanielfenta@gmail.com"         # Replace with your Gmail
msg['To'] = user_email
msg['Subject'] = "Your News Alerts"
msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("bethelhemdanielfenta@gmail.com", "vvoc jmsu lysb atvv")  # Replace with app password
    server.send_message(msg)
    server.quit()
    print(f"Email sent to {user_email} successfully!")
except Exception as e:
    print("Failed to send email:", e)

# Print all filtered articles after email is sent
for i, art in enumerate(filtered_articles, start=1):
    print(f"\n--- Article {i} ---")
    print("Title:", art['title'])
    print("Link :", art['link'])
    print("Description (first 150 chars):", art['description'][:150])
    print("Published:", art['published'])
