import pandas as pd
import numpy as np
import pickle
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic

class DataPrep(object):
    def __init__(self):
        #get coord list
        with open("./parameters/coord_list.txt", "r") as file:
            self.coord_list = eval(file.readline())

        with open("./parameters/x_cols.txt", "r") as file:
            self.x_cols = eval(file.readline()).encode("utf-8")


    def pipeline(self, df):
        #function that performs geocode
        def do_geocode(address, attempt=1, max_attempts=5):
            try:
                return locator.geocode(address, addressdetails=True)
            except GeocoderTimedOut:
                if attempt <= max_attempts:
                    return do_geocode(address, attempt=attempt+1)
                raise

        #function to get_key ou of location column
        def get_key(x, key):
            try:
                result = x.raw['address'][key]
            except KeyError:
                result ='unknown'
            return result    

        #original code found on https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
        def to_1D(series):
            return pd.Series([x for _list in series for x in _list])

        def boolean_df(item_lists, unique_items):
        # Create empty dict
            bool_dict = {}
            
            # Loop through all the tags
            for i, item in enumerate(unique_items):
                
                # Apply boolean mask
                bool_dict[item] = item_lists.apply(lambda x: item in x)
                    
            # Return the results as a dataframe
            return pd.DataFrame(bool_dict)

        #get distance of propertie to the beach
        def get_distance(x):
            values = []
            for i in self.coord_list:
                values.append(geodesic(x, i).km)
            return min(values)

        #changing names from Brazilian Portuguese to English
        df.replace({'property_type' : { 'apartamento' : 'apartment', 'casa' : 'house'}}, inplace = True)

        #creating geopy objects
        locator = Nominatim(user_agent = 'myGeocoder')
        geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

        #getting location column
        df['location'] = df['address'].apply(lambda x: do_geocode(x))

        #removing not found locations
        df = df[df.location.notna()]

        #getting neighborhood and actual city
        df['neighborhood'] = df.location.apply(lambda x: get_key(x,'suburb'))
        df['city'] = df.location.apply(lambda x: get_key(x, 'city'))

        #getting latitude and longitude
        df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)

        #dropping unnecessary columns
        df.drop(columns = ['location', 'address'], inplace = True)

        #filtering only Recife
        df = df[df.city == 'Recife']
        
        #doing eval
        df["extra_contents"] = df["extra_contents"].apply(eval)

        #now we won't need the city column anymore, so we'll remove it
        df.drop(columns = ['city'], inplace = True)

        #creating dummy columns for each variable inside the extra_contents column            
        extra_contents_df = boolean_df(df.extra_contents, to_1D(df.extra_contents)).astype(int)

        #using pandas concat to add the new column to our dataset
        df = pd.concat([df, extra_contents_df], axis=1)
        df.drop(columns = ['extra_contents'], inplace = True)

        #naming original columns of our dataframe
        selected_columns = ['property_type', 'area', 'bathrooms', 'bedrooms', 'parking_spots', 'neighborhood','point', 'Mais de um andar',
        'Mobiliado', 'Churrasqueira', 'Cozinha', 'Piscina']
        
        #adding main 4 extra columns if they were not in the original df
        for col in selected_columns:
            if col not in df.columns:
                df[col] = 0

        #filtering columns
        df = df[selected_columns]

        #renaming columns
        df.columns = ['property_type', 'area', 'bathrooms', 'bedrooms', 'parking_spots',
        'neighborhood', 'point', 'more_than_1_floor', 'furnished',
        'barbecue_grill', 'kitchen', 'pool']

        #get beach distance
        df['beach_distance'] = df.point.apply(lambda x: get_distance(x))

        #getting latitude and longitude columns for visualization and dropping unnecessary columns
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
        df.drop(columns = ['altitude', 'point'], inplace = True)

        #getting dummy columns
        df1 = df.copy()
        df = pd.get_dummies(df1)
        
        #loop to fill not used dummy columns
        for col in self.x_cols:
            if col not in df.columns:
                df[col] = 0
        
        #ordering columns just like the model
        df = df[self.x_cols]

        #transforming area using np log as explained in the eda
        df['area'] = np.log(df.area)


        return df 









