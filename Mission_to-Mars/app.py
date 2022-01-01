from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Root route to query Mongo DB and pass mars data into HTML template to display
@app.route("/")
def index():
    scraped_mars_data = mongo.db.scraped_mars_data.find_one()
    return render_template("index.html", scraped_mars_data=scraped_mars_data)

# Scrape route to import scrape_mars.py and call scrape function,
### and store return value in Mongo as python dictionary
@app.route("/scrape")
def scraper():
    scraped_mars_data = mongo.db.scraped_mars_data
    scraped_mars_data_entry = scrape_mars.scrape()
    scraped_mars_data.update({}, scraped_mars_data_entry, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)