from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import replicapredictor as model
import pandas as pd
import time

url = "https://nusqzacpsvrkxchbgnec.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51c3F6YWNwc3Zya3hjaGJnbmVjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1ODMzNjQsImV4cCI6MjA2NzE1OTM2NH0.ohWErLIhR0BphWFgi9u9yMaPXmyz1xQb8eZRxYjIzsA"
#Url and API key for the database I created storing data about various items

supabase: Client = create_client(url,key)

app = Flask(__name__)
app.config['DEBUG'] = True

    
@app.route("/")
def hello_world():
    return render_template("replicapage.html")

@app.route("/submit", methods = ["POST"])
def submit():
    item = request.form.get("items")
    market = (request.form.get("markets"))
    price = (request.form.get("price"))
    reviews = (request.form.get("reviews"))
    rating = (request.form.get("rating"))
    proof = (request.form.get("proof"))
    justify = (request.form.get("justify"))

    load_dotenv()

    response = (
    supabase.table("ItemListings")
    .select("*")
    .eq("ItemID",item)
    .csv()
    .execute()
    )

    features = []
    features.append(price)
    features.append(reviews)
    features.append(rating)
    features.append(market)
    features.append(proof)
    features.append(justify)


    repfeatures = []
    repfeatures.append(features)

    time.sleep(2)
    result = model.replicamodel(response.data,(pd.DataFrame(repfeatures, columns = model.featurenames)))


    return jsonify({'result': (str(result))})



    

if __name__ == "__main__":
    app.run(debug = True)