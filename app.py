# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os
# Create an instance of Flask app
app = Flask(__name__)



# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# Create route that renders index.html template and finds documents from mongo

@app.route("/")
def home():
#Find data
    mars_dict = mongo.db.mars_dict.find_one()

#Return template and Data
    return render_template("index.html",mars_dict=mars_dict)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 
#run Scrapped function
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape_mars_news()  
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrap_mars_weather()
    mars_data = scrape_mars.scrape_mars_fact()
    mars_data = scrape_mars.scrape_mars_hemisphere()

    mars_dict.update({}, mars_data, upsert=True)

    return redirect("/",code=302)

if __name__ == "__main__":
    app.run(debug=True) 