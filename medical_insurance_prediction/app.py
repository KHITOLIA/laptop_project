from flask import Flask ,render_template, request, redirect
import pickle
import numpy as np
from db import Database

app = Flask(__name__)

with open("pipe_lr.pkl", "rb") as f:
    pipe = pickle.load(f)
obj = Database()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
def prediction():
    if request.method == "POST":
        age = request.form['age']
        sex = request.form['sex']
        bmi = request.form['bmi']
        children = request.form['children']
        smoker = request.form['smoker']
        region = request.form['region']
        pred = np.round(pipe.predict([[age, sex, bmi, children, smoker, region]])[0], 2)
        obj.save_predictions(age, sex, bmi, children, smoker, region, pred)
        return render_template("predict.html", pred = pred)
    
    return render_template("predict.html")

if __name__ == "__main__":
    app.run(debug = True)
