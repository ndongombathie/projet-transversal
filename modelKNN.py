from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score 
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("air_quality.csv")
print(data.head())
x = data[["latitude", "longitude"]]
y = data['iqr']
#y = y['categorie_iqa'].map({'Bonne':0,'moderée':1,'Mauvaise':2,'Très mauvaise':3,'Extrêmement mauvaise':4})
#imputation des valeurs manquantes pour les colonnes "pm02_corrected", "pm10_corrected", "atmp_corrected", "rhum_corrected" et "rco2_corrected"
x = x.fillna(x.mean())
y = y.fillna(y.mean())

#afficher les valeur nan
print("Valeurs manquantes dans x:", x.isna().sum())
print("Valeurs manquantes dans y:", y.isna().sum())
print(x.head())


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


model = KNeighborsRegressor(n_neighbors=3,weights="distance")
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

y_test = model.predict(x_test)
print(y_test)


