import pandas as pd
import pickle
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic



class DataPrep(object):
     def __init__(self):
        #get coord list
        with open("coord_list.txt", "r") as file:
        coord_list = eval(file.readline())





    def pipeline(self, df):
            #cuntion that performs geocode
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
            for i in coord_list:
                values.append(geodesic(x, i).km)
            return min(values)

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
        df.drop(columns = ['location', 'title', 'address'], inplace = True)

        #filtering only Recife
        df = df[df.city == 'Recife']

        #now we won't need the city column anymore, so we'll remove it
        df.drop(columns = ['city'], inplace = True)

        #creating dummy columns for each variable inside the extra_contents column            
        extra_contents_df = boolean_df(df.extra_contents, to_1D(df.extra_contents)).astype(int)

        #using pandas concat to add the new column to our dataset
        df = pd.concat([df, extra_contents_df], axis=1)
        df.drop(columns = ['extra_contents'], inplace = True)

        #summing fee and rent column
        df['rent'] = df['rent'] + df['fee']
        df.drop(columns = ['fee'], inplace = True)

        #naming original columns of our dataframe except for rent
        selected_columns = ['property_type', 'area', 'bathrooms', 'bedrooms', 'parking_spots', 'neighborhood','point', 'Mais de um andar',
        'Mobiliado', 'Churrasqueira', 'Cozinha', 'Piscina']

        #renaming columns
        df.columns = ['property_type', 'area', 'bathrooms', 'bedrooms', 'parking_spots',
        'neighborhood', 'point', 'rent', 'more_than_1_floor', 'furnished',
        'barbecue_grill', 'kitchen', 'pool']

        #get beach distance
        df['beach_distance'] = df.point.apply(lambda x: get_distance(x))

        #getting latitude and longitude columns for visualization and dropping unnecessary columns
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
        df.drop(columns = ['altitude', 'point'], inplace = True)
        return df 












