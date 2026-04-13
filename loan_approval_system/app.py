from flask import Flask, render_template, redirect, request
from src.db import Database
import pickle


app = Flask(__name__)
obj = Database()
with open('svm.pkl', 'rb') as file:
    pipe = pickle.load(file)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == 'POST':
        Gender = request.form['Gender']
        Married  = request.form['Married']
        Dependents = request.form['Dependents']
        Education = request.form['Education']
        Self_Employed = request.form['Self_Employed']
        Loan_Amount = request.form['Loan_Amount']
        Loan_Amount_Term = request.form['Loan_Amount_Term']
        Credit_History = request.form['Credit_History']
        Property_Area = request.form['Property_Area']
        Family_Income= request.form['Family_Income']

        Loan_Status = pipe.predict([[Gender, Married, Dependents,Education, Self_Employed, Loan_Amount, Loan_Amount_Term, Credit_History
                                     ,Property_Area, Family_Income]])[0]
        
        obj.save_predictions(Gender, Married, Dependents, 
                                     Education, Self_Employed, Loan_Amount, Loan_Amount_Term, Credit_History
                                     ,Property_Area, Family_Income, Loan_Status)
        
    return render_template('predict.html', pred = Loan_Status)
        


if __name__ == "__main__":
    app.run(debug=True)