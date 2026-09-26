
import streamlit as st
import requests
import pandas as pd
import numpy as np
import io

# --- Configuration --- #
# Use the service name defined in docker-compose.yml for the backend
# In a GitHub Codespace, services communicate via their service names.
BACKEND_BATCH_URL = "http://backend:8000/predict"
BACKEND_SINGLE_URL = "http://backend:8000/predict_single"

st.set_page_config(layout="wide")
st.title("Airbnb Rental Price Prediction")

st.write("Enter the details below for a single prediction or upload a CSV for batch predictions.")

# --- Input Form for Single Prediction --- #
st.header("Single Prediction")
with st.form("single_prediction_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        accommodates = st.number_input("Accommodates", min_value=1, max_value=16, value=2, key='s_accommodates')
        bathrooms = st.number_input("Bathrooms", min_value=0.5, max_value=8.0, value=1.0, step=0.5, key='s_bathrooms')
        bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=1, key='s_bedrooms')

    with col2:
        beds = st.number_input("Beds", min_value=1, max_value=18, value=1, key='s_beds')
        room_type = st.selectbox("Room Type", ['Entire home/apt', 'Private room', 'Shared room', 'Hotel room'], key='s_room_type')
        cancellation_policy = st.selectbox("Cancellation Policy", ['strict', 'moderate', 'flexible'], key='s_cancellation_policy')

    with col3:
        minimum_nights = st.number_input("Minimum Nights", min_value=1, max_value=1000, value=1, key='s_minimum_nights')
        number_of_reviews = st.number_input("Number of Reviews", min_value=0, max_value=1000, value=10, key='s_number_of_reviews')
        instant_bookable = st.checkbox("Instant Bookable", value=True, key='s_instant_bookable')
        host_listings_count = st.number_input("Host Listings Count", min_value=0, max_value=500, value=1, key='s_host_listings_count')

    single_submitted = st.form_submit_button("Get Single Prediction")

    if single_submitted:
        input_data = {
            "room_type": room_type,
            "accommodates": accommodates,
            "bathrooms": bathrooms,
            "cancellation_policy": cancellation_policy,
            "minimum_nights": minimum_nights,
            "number_of_reviews": number_of_reviews,
            "bedrooms": bedrooms,
            "beds": beds,
            "instant_bookable": instant_bookable,
            "host_listings_count": host_listings_count
        }

        st.write("Sending single prediction request to backend...")
        try:
            response = requests.post(BACKEND_SINGLE_URL, json=input_data)
            if response.status_code == 200:
                prediction = response.json() # Single float directly
                st.success(f"Predicted Rental Price: ${prediction:,.2f}")
            else:
                st.error(f"Error from backend: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend service. Make sure it is running.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


st.markdown("--- ")

# --- File Uploader for Batch Prediction --- #
st.header("Batch Prediction (Upload CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.write("Processing CSV for batch prediction...")
    try:
        # Read CSV file into pandas DataFrame
        dataframe = pd.read_csv(uploaded_file)
        st.write("Input CSV Data:")
        st.dataframe(dataframe.head())

        # Convert DataFrame to list of dictionaries for JSON payload
        batch_input_data = dataframe.to_dict(orient='records')

        st.write("Sending batch prediction request to backend...")
        response = requests.post(BACKEND_BATCH_URL, json=batch_input_data)

        if response.status_code == 200:
            batch_predictions = response.json()
            predictions_df = pd.DataFrame({"Predicted Price": batch_predictions})
            st.success("Batch predictions received!")
            st.dataframe(predictions_df)
        else:
            st.error(f"Error from backend: {response.status_code} - {response.text}")

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
    except pd.errors.ParserError:
        st.error("Could not parse the CSV file. Please ensure it's a valid CSV format.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend service. Make sure it is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.markdown("""
--- 
### How to use:
**Single Prediction:**
1. Fill in the details of the Airbnb rental in the form above.
2. Click 'Get Single Prediction' to receive an estimated rental price from the Flask backend.

**Batch Prediction:**
1. Prepare a CSV file with multiple rows of rental features (matching the format expected by the model).
2. Upload the CSV file using the 'Choose a CSV file' button.
3. The predicted prices for each row in the CSV will be displayed.
""")
