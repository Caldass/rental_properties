import pickle
from flask import Flask, request
import pandas as pd

#loading model
model = pickle.load(open('../model_building/model_file.pkl', 'rb'))

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

    #prediction
    pred = model.predict(df_raw)
    df_raw['prediction'] = pred

    return df_raw.to_json(orient = 'records')

if __name__ == '__main__':
    #start flask
    app.run(host = 'localhost', port = '5000')

