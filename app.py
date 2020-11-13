from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

conn = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index_page():
    data = conn.mars_db.mars_collection.find_one()
    return render_template("index.html", data=data)

@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    conn.mars_db.mars_collection.update({}, mars_data, upsert = True)
    return redirect("/")

if __name__ == "__main__":
    spp.run(debug=True)


