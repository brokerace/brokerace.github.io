from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

# create app
app = Flask(__name__)

#connect to mongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

#create directory
@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html", data = data)

#get scraping
@app.route("/scrape")
def scraper():
    refresh = mongo.db.data
    refresh_data = scrape()
    refresh.update({}, refresh_data, upsert=True)
    return redirect("/", code=302)

#debug
if __name__ == '__main__':
    app.run(debug=True)
