News Alert Keyword Filter – Flask App

A simple web-based tool that fetches articles from multiple RSS feeds, filters them by user-provided keywords, displays the results on the page, and sends the filtered list to a provided email address.

The two RSS feeds I used:

1. Techcrunchy - https://techcrunch.com/feed/
2. BBC Technology - http://feeds.bbci.co.uk/news/technology/rss.xml

This project is built with Flask, Feedparser, and Gmail SMTP (requires an App Password).

Features

Fetches articles from multiple RSS feeds

Keyword-based filtering (case-insensitive)

Displays filtered results in the UI

Sends filtered results to the user's email

Simple Flask frontend

Tech Stack

Python 3.13+

Flask

SQLite

Feedparser

SMTP (Gmail)

python-dotenv

Installation
1. Clone the repository
git clone https://github.com/Bethel-21/News-alert.git
cd <your-repo>

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux / Mac
# OR
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

Environment Variables (.env)

Create a file named .env in the project root:

EMAIL_USER=yourgmail@gmail.com
EMAIL_PASS=your_app_password

Important:

You must create a Gmail App Password.
Normal Gmail passwords will NOT work with SMTP.

To get your App Password:

Enable 2-Step Verification on your Google account

Visit: https://myaccount.google.com/apppasswords

Generate a 16-digit password

Paste it in your .env file

Running the App
python app.py


Navigate to:

http://127.0.0.1:5000/
