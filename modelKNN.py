from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score 
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt

#charger les données depuis minio
data = pd.read_csv("air_quality.csv")
print(data.head())
x = data[["latitude", "longitude"]]
y = data[['iqr','pm25','pm10','co2','no2','so2','o3']]

x = x.fillna(x.mean())
y = y.fillna(y.mean())

#afficher les valeur nan
print("Valeurs manquantes dans x:", x.isna().sum())
print("Valeurs manquantes dans y:", y.isna().sum())
print(x.head())



""" #visualisation les capteurs sur une carte avec latitude et longitude
plt.scatter(data['longitude'], data['latitude'], c=data['pm10'], cmap='viridis')
plt.colorbar(label='PM10')  
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('PM10 concentration')
plt.show() """

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


model = KNeighborsRegressor(n_neighbors=3,weights="distance")
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

y_test = model.predict([[14.7936825,-16.9817974]])
data_test = pd.DataFrame(y_test, columns=y_train.columns)
print(data_test)


