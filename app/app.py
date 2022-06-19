from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scraping import ScraperHelper

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    scraper = ScraperHelper()
    mars_data = scraper.scrape_info()

    # Update the Mongo database using update and upsert=True
    mars_info = mongo.db.mars_info
    mars_info.update_one({}, {"$set": mars_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
