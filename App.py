import streamlit as st
import pandas as pd
import pickle
import os

# Function to load a file
def load_file(path, file_type="Pipeline/Model"):
    if os.path.exists(path):
        try:
            with open(path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            st.error(f"Error loading {file_type}: {e}")
            return None
    else:
        st.error(f"{file_type} file not found: {path}")
        return None

# Paths to files
pipeline_path = r'https://github.com/unaib-tech/Data-Science-Capstone-Project/blob/main/car_price_pipeline.pkl'
model_path = r'https://github.com/unaib-tech/Data-Science-Capstone-Project/blob/main/model.pkl'

# Load files
pipeline = load_file(pipeline_path, "Pipeline")
model = load_file(model_path, "Model")

# Streamlit App
st.title("Car Price Prediction App")

# User inputs
year = st.number_input("Year of Manufacture", min_value=1900, max_value=2024, value=2018)
km_driven = st.number_input("Kilometers Driven", min_value=0, value=25000)
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission Type", ["Manual", "Automatic"])
owner = st.selectbox("Owner Type", ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"])

# Predict button
if st.button("Predict Selling Price"):
    if pipeline and model:
        # Create DataFrame
        input_data = pd.DataFrame([[year, km_driven, fuel, seller_type, transmission, owner]],
                                  columns=['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner'])

        try:
            # Predict
            prediction = pipeline.predict(input_data)
            st.success(f"Predicted Selling Price: ₹{prediction[0]:,.2f}")
        except Exception as e:
            st.error(f"Error during prediction: {e}")
    else:
        st.error("Files not loaded correctly. Check paths and try again.")

