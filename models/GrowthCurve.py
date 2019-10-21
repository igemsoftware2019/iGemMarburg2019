#    Copyright 2019, iGEM Marburg 2019
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np 
import pandas as pd 
import sklearn
import operator
#from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
degree_polynomial = 8
size_test = 1

data_model = pd.read_csv("data_model_clean_neu.csv")
data_prep = data_model.drop("Unnamed: 0", axis = 1)


# Now I want to add data that shows the constraints of the system, so I will engineer fake data to correctly predict everything
# Format is doubling time, light, rpm, co2, temp
low_light = [1000,100,220,5,41]
high_light = [1000, 3000, 220, 5, 41]
low_rpm = [1000,1500,30,5,41]
high_rpm = [1000,1500,300,5,41]
low_co2 = [1000,1500,220,1,41]
high_co2 = [1000,1500,220,20,41]
low_temp = [1000,1500,220,5,30]
high_temp = [1000,1500,220,5,50]

boundary = []
boundary.append(high_temp)
boundary.append(low_temp)
boundary.append(high_co2)
boundary.append(low_co2)
boundary.append(high_rpm)
boundary.append(low_rpm)
boundary.append(high_light)
boundary.append(low_light)
boundary = pd.DataFrame(boundary)

boundary.columns = ["doubling_time","light_intensity","rpm","co2","temp"]
result = pd.concat([boundary, data_prep])

# Now we need to split the data into x and y
x = data_prep.drop(["doubling_time"], axis = 1)
y = data_prep["doubling_time"]


# To troubleshoot and once we have enough data, this is a very easy and sometimes faulty way to generate a train_test_split
# For an advanced train test split the sklearn functionality would be used
x_train = x[:-size_test]
x_test = x[-size_test:]
y_train = y[:-size_test]
y_test = y[-size_test:]

# Now we define the polynomial and the data that we want to predict
poly = PolynomialFeatures(degree=degree_polynomial)
light_pred = [ 1388, 1541, 1750, 1850]
rpm_pred = [ 147, 147, 147, 147]
co2_pred = [ 3.8, 3.8, 3.8, 3.8]
temp_pred = [ 40.5, 40.5, 40.5, 40.5]

to_predict = pd.DataFrame({"light_pred":light_pred, "rmp_pred":rpm_pred, "co2_pred":co2_pred, "temp_pred":temp_pred})
to_predict_pol = poly.fit_transform(to_predict)

#Now the actual model is trained as a pipeline for the polynomial features
model = Pipeline([('poly', PolynomialFeatures(degree=degree_polynomial)), ('linear', LinearRegression(fit_intercept=True, normalize = True))])
model = model.fit(x, y)
#print(model.named_steps["linear"].coef_)
predictions = model.named_steps["linear"].predict(to_predict_pol)
#print("hello")
score = model.score(x_test, y_test)

# Now the prediction is done and printed together with score and diagnose values for the model
to_predict = pd.DataFrame(to_predict)
to_predict["predictions"] = predictions
print(to_predict)
print(score)
print(predictions)

y_poly_pred = model.predict(x)
rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
r2 = r2_score(y,y_poly_pred)
print(rmse, r2)

#pred_test = model.predict(x_test)
#print(pred_test)
#print(y_test)
#print(data_prep.to_html())