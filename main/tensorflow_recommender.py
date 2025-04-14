import tensorflow as tf
import numpy as np

# Load model and encoders
model = tf.keras.models.load_model('main/recommendation_model.h5')
product_classes = np.load('main/product_classes.npy', allow_pickle=True)
recommendation_classes = np.load('main/recommendation_classes.npy', allow_pickle=True)

def get_recommendation(product_name):
    try:
        # Find index of product
        product_index = np.where(product_classes == product_name)[0][0]
        
        # Predict
        prediction = model.predict(np.array([product_index]))
        recommended_index = np.argmax(prediction)
        
        return recommendation_classes[recommended_index]
    except IndexError:
        return "Product not found in database."
