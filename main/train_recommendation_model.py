import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os

# Load the data
data = pd.read_csv('recommendation_data.csv')

# Encode text labels
product_encoder = LabelEncoder()
recommendation_encoder = LabelEncoder()

data['Product_encoded'] = product_encoder.fit_transform(data['Product'])
data['Recommendation_encoded'] = recommendation_encoder.fit_transform(data['Recommendation'])

# Features and labels
X = data['Product_encoded'].values
y = data['Recommendation_encoded'].values

# Neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=len(product_encoder.classes_), output_dim=10, input_length=1),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(len(recommendation_encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=100, verbose=1)

# Save the model and encoders
model.save('main/recommendation_model.h5')
np.save('main/product_classes.npy', product_encoder.classes_)
np.save('main/recommendation_classes.npy', recommendation_encoder.classes_)
