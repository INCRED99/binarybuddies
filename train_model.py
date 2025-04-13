import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Dummy dataset: [electricity, car_km, meat_meals, flights]
X = np.array([
    [10, 20, 3, 2],
    [5, 15, 2, 1],
    [20, 30, 5, 4],
    [7, 10, 1, 0],
    [15, 25, 4, 3],
])

# Labels: Higher means higher carbon footprint
y = np.array([60, 30, 80, 20, 70])

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, 'main/ml_model.pkl')
print("Model trained and saved!")
