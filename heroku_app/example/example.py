import pandas as pd
import requests
import json

#prediction request url
url = 'https://rental-properties.herokuapp.com/predict'

#headers
headers = {'Content-type': 'application/json'}

#input example
input_df = pd.DataFrame({'property_type': ['apartamento'], 'address' : ['Avenida Boa Viagem, 5822 - Boa Viagem, Recife - PE'], 'area' : [160], 'bathrooms': [5],
                  'bedrooms' : [4], 'bathrooms' : [2] , 'parking_spots' : [3], 'extra_contents' : ["['Mais de um andar', 'Mobiliado', 'Churrasqueira', 'Cozinha', 'Piscina']"]})

#transform df into json format
df_json = input_df.to_json(orient = 'records')

#make request to server
r = requests.post( url = url , data = df_json, headers =headers)

#output dataframe with prediction
output = pd.DataFrame(r.json(), columns = r.json()[0].keys())

#Print result
print('Property rent is R$ %.2f' % output.prediction[0])