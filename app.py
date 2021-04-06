from flask import Flask, render_template, request
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open("random_forest.pkl","rb"))


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])
def predict():
    fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        owner=int(request.form['Owner'])
        fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(fuel_Type_Petrol=='Petrol'):
                fuel_Type_Petrol=1
                fuel_Type_Diesel=0
        else:
            fuel_Type_Petrol=0
            fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[present_Price,Kms_Driven2,owner,Year,fuel_Type_Diesel,fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True,port = 5001)

