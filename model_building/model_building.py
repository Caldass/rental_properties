import pandas as pd 
import csv
import numpy as np
import time
import pickle
from scipy.stats import randint
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import RandomizedSearchCV

#reading eda df
df = pd.read_csv('./eda/eda_df.csv')

#removing latitude and longitude since they're highly correlated to beach_distance as seen in the eda
df.drop(columns = ['latitude', 'longitude'], inplace = True)

#getting dummy columns
df_dum = pd.get_dummies(df)

np.random.seed(101)

X = df_dum.drop(columns = ['rent'], axis = 1)
y = df_dum.rent.values

x_cols = list(X.columns)

#saving X columns to file to use it later on our api
#with open("./heroku_app/parameters/x_cols.txt", "w") as file:
#    file.write(x_cols)

pickle.dump(x_cols, open('./heroku_app/parameters/x_cols.pkl', 'wb'))



#split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#creating models variable to iterate through each model and print result
models = [LinearRegression(), Lasso(alpha=0.1), RandomForestRegressor(), GradientBoostingRegressor()]

names = ['Linear Regression', 'Lasso Regression', 'Random Forest', 'Gradient Boost']

#loop through each model and print train score and elapsed time
for model, name in zip(models, names):
    start = time.time()
    scores = cross_val_score(model, X_train, y_train ,scoring= 'neg_mean_absolute_percentage_error', cv=5)
    print(name, ":", "%0.2f, +- %0.2f" % (scores.mean(), scores.std()), " - Elapsed time: ", time.time() - start)

#tuning random forest
rf = RandomForestRegressor()

parameters = {'n_estimators':randint(10,300), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

rs = RandomizedSearchCV(rf,parameters,scoring='neg_mean_absolute_percentage_error',cv=3, n_iter = 250)
start = time.time()

#printing best fits and time elapsed
rs.fit(X_train,y_train)
print(rs.best_score_, rs.best_params_,  time.time() - start)

#Fitting other regressors
lr = Lasso(alpha = 0.1)
lr.fit(X_train,y_train)

gb = GradientBoostingRegressor()
gb.fit(X_train,y_train)

# test models on unseen data 
tpred_lr = lr.predict(X_test)
tpred_rf = rs.best_estimator_.predict(X_test)
tpred_gb = gb.predict(X_test)

print(mean_absolute_percentage_error(y_test,tpred_lr))
print(mean_absolute_percentage_error(y_test,tpred_rf))
print(mean_absolute_percentage_error(y_test,tpred_gb))

#retraining final model on full data
rs.best_estimator_.fit(X, y)

#saving model
pickle.dump(rs, open('./heroku_app/model/model_file.pkl', 'wb'))