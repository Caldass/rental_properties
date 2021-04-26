# Recife's Properties Rent Estimator - Project Overview
- Deployed tool that estimates the rent of a property in the city of Recife (Brazil) (MAPE ~ 2.2%) to help people negotiate and evaluate rent prices.
- Scraped over 4000 properties data from https://www.vivareal.com.br/ using BeatifulSoup and Selenium.
- Engineered features like latitude, longitude and beach distance using Geopy and Geopandas and also extracted extra contents about the property in order to help quantify the rent.
- Built models and optimized Random Forest Regressor in order to reach the best model to predict rent.
- Productionized the model using Flask and Heroku.


## Code and Resources Used
**Python version**: 3.7

**Packages**: Pandas, Numpy, Geopy, Geopandas, Flask, Sklearn, Pickle, Plotly, Matplotlib, Folium, BeatifulSoup, Selenium.

**Flask and Heroku productionization**: [Meigarom's Youtube videos](https://www.youtube.com/channel/UCar5Cr-pVz08GY_6I3RX9bA) on the theme really helped building the final product. 

## Web Scraping
Used BeautifulSoup and Selenium to scrape over 4000 posts on Recife's rental properties from https://www.vivareal.com.br/. The data was scrapped between the 12th and the 20th of April 2021. For each post the following data was retrieved:

- **title** - Property's description.
- **address** - Property's address.
- **area** - Property's area in m².
- **bathrooms** - Property's amount of bathrooms.
- **bedrooms** - Property's amount of bedrooms.
- **parking_spots** - Property's amount of parking spots.
- **extra_contents** - Property's extra information i.e. if it had a pool or elevator.
- **rent** - Property's rent in R$.
- **fee** - Property's fee in R$.

## Data cleaning
After scrapping the data multiple files were generated. Those files were grouped and had their duplicates removed to create the raw data frame used in the project. Here's some of the changes applied to the data:

- Filled nulls on the extra_contents column with empty lists.
- Filled nulls on the fee column with 0.
- Removed currency simbols from the rent and fee columns.
- Removed string characters from numerical columns and turned them into integers.  

## Feature Engineering
Created new features using Geopy, Geopandas and extra_contents and also modifyed existing columns in order to help better understand the data and quantify the rent column. Here's the features created:

- **property_type** - Defines if a property is a house or a apartment.
- **neighborhood** - Property's neighborhood.
- **more_than_1_floor** - 1 if property has more than one floor.
- **furnished** - 1 if property is furnished.
- **barbecue_grill** - 1 if property has a barbecue grill.
- **kitchen** - 1 if property has a kitchen.
- **pool** - 1 if property has a pool.
- **beach_distance** - Property's distance to the beach.
- **latitude**
- **longitude**



## EDA
In this step we managed to:
- Find some irregularities in our data through data visualization that we couldn't find in the Data Cleaning step.
- Explore the data in order to better understand it.
- Perform tests such as Shapiro-Wilks test and checked for normality in our data.
- Normalize rent and area column using log.

Here are some highlights of the data exploration:
![alt text](https://github.com/Caldass/rental_properties/blob/main/images/cmap.png "Correlation Heatmap")
![alt text](https://github.com/Caldass/rental_properties/blob/main/images/map.png "Recife Map")
![alt text](https://github.com/Caldass/rental_properties/blob/main/images/median-rent.png "Median rent by neighborhood")
![alt text](https://github.com/Caldass/rental_properties/blob/main/images/rent-distribution.png "Rent distribution")
![alt text](https://github.com/Caldass/rental_properties/blob/main/images/recife_map.html "Recife Map")


## Model Building

In this step I removed the latitude and longitude columns to avoid correlation between independent variables and split the data between training and test set with a test size of 20%. Here are the models used:
- Multiple Linear Regression and Lasso Regression - Baselines for the model. Linear Regresssion was expected to have bad results  due to the number of features and sparsity in the data, that's why we used a regularized regression model like Lasso.
- Random Forest Regressor - Tree based ensemble model expected to work well due to the sparsity of the data.
-  Gradient Boost Regressor - Just like Random Forest, a tree based ensemble model expected to work well due to the sparsity of the data.

To evaluate the model I chose the Mean Absolute Percentage Error (MAPE), since it's a metric that's not affected that much by outliers and it's easy to interpret. Basically it says how off our predictions were on average.


### Model Results
Linear Regression had terrible results as expected due to the number of features after dummy encoding, an issue Lasso Regression did not went through. Random Forest beat the other models so it was the chosen model to be tuned. Here are the results:
 - **Lasso Regression** - MAPE = 3.7%
 - **Random Forest Regressor** - MAPE = 2.2%
 - **Gradient Boost Regressor** - MAPE = 2.5%

## Productionization
In this step I built a Flask API endpoint which I deployed to a heroku application. The application is available and hosted at https://rental-properties.herokuapp.com/predict. The input should be as follows the example:
- **property_type** - _'apartamento'_ or _'casa' __(apartment or house)_.
- **address** - _'Avenida Boa Viagem, 5822 - Boa Viagem, Recife - PE'_ (street name, number - neighborhood, Recife - PE).
- **area** - 160 (integer number that represents area).
- **bedrooms** - 4 (integer number that represents bedrooms).
- **parking_spots** - 3 (integer number that represents parking spots).
- **extra_contents** - _"['Mais de um andar', 'Mobiliado', 'Churrasqueira', 'Cozinha', 'Piscina']"_ (More than one floor, Furnished, Barbecue grill, Kitchen, Pool).

The **property_type** and the **extra_contents** inputs are in Portuguese since this project is aimed at the residents of Recife but written in English so that it could be helpful and accessible to anyone. 

Under _heroku_app/example/example.py_ there's input example to help the understanding of the request.

