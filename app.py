from flask import Flask, render_template, request
from send_news import fetch_all_articles 
from send_news import filter_articles 
from send_news import send_email
import sqlite3



def get_db_connection():
    conn = sqlite3.connect("subscriptions.db")
    conn.row_factory = sqlite3.Row  # So you can access columns by name
    return conn



app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        email = request.form.get("email")
        keywords = request.form.get("keywords")
        keywords_list = [k.strip() for k in keywords.split(",")]


        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subscribers (email, keywords) VALUES (?, ?)",
            (email, ",".join(keywords_list))

        )
        conn.commit()
        conn.close()


        

        

        all_articles = fetch_all_articles()
        filtered = filter_articles(all_articles, keywords_list)

   
        send_status = send_email(email, filtered)


      # renders the html page to display the filtered fields
        return render_template(
        "index.html",
        email=email,
        keywords=keywords,
        results=filtered,
        sent=send_status
    )
     # the homepage first displays no email, keyword, and result
    return render_template("index.html", email=None, keywords=None, results=None)


        

if __name__ == "__main__":
    app.run(debug=True)
