import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



@app.route("/")
def home():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)


@app.route('/scrape')
def scrape():
    
    mars = mongo.db.mars
    browser=scrape_mars.init_browser
    mars_data = scrape_mars.scrape(browser)
    mongo.db.collection.update({},mars_data,upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)


