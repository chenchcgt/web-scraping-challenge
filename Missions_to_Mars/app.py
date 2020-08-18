from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# connect to mongo db
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# connect to scrape python function

@app.route('/scrape')
def scrape():
    
    mars_dict = scrape_mars.scrape()
    mongo.db.collection.update({},mars_dict,upsert = True)

    return redirect('/', code=302)

# home page with all info

@app.route('/')
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template('index.html',mars_info = mars_data)


if __name__ == "__main__":
    app.run(debug=True)