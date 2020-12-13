import sys
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_DB")



@app.route("/")
def home():
    mars = mongo.db.mars_dict.find_one()
    print(mars)
    return render_template("index.html", mars= mars)


@app.route('/scrape')
def scrape():
    browser = scrape_mars.init_browser()

    mars_data = mongo.db.mars_dict

    mars_data = scrape_mars.scrape()
    mars_data.update({},mars_data,upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)


