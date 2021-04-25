import pickle
from flask import Flask, request
import pandas as pd
from data_prep.data_prep import DataPrep
import os

#loading model
model = pickle.load(open('./model/model_file.pkl', 'rb'))

#instanciate flask
app = Flask(__name__)

#endpoint
@app.route('/predict', methods = ['POST'])
def predict():
    test_json = request.get_json()

    #get data
    if test_json:
        if isinstance(test_json, dict): #unique value
            df_raw = pd.DataFrame(test_json, index = [0])
        else:
            df_raw = pd.DataFrame(test_json, columns = test_json[0].keys())
    
    #instanciate pipeline
    pipe = DataPrep()
    df1 = pipe.pipeline(df_raw)

    #prediction
    pred = model.predict(df1)
    df1['prediction'] = pred

    return df1.to_json(orient = 'records')

if __name__ == '__main__':
    #start flask
    port = os.environ.get('PORT', 3000)
    app.run(host = 'localhost', port = port)

