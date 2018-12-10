# import necessary libraries
from flask import Flask, render_template, request, redirect,  url_for
import pymongo
import scrapeMars 

# create an instance of flask app
app = Flask(__name__)

client = pymongo.MongoClient()
db = client.astronomy_db
collection = db.mars

# create route that renders the html template
@app.route("/")
def home():
    data = db.collection.find_one()
    return render_template('index.html',data=data)


@app.route("/scrape")
def scrape():

    db.collection.delete_many({})
    scrappedData = scrapeMars.scrape()
    print(scrappedData)
    db.collection.insert_one(scrappedData)
    print(list(db.collection.find()))
    return redirect(url_for('home'))

    # return redirect("http://www.localhost:5000/", code=302)


# run as a python script
if __name__ == "__main__":
    app.run(debug=True)
