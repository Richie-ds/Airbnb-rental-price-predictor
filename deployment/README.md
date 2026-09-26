
# Airbnb Rental Price Predictor

This repository contains the deployment files for an Airbnb rental price prediction application, consisting of a Flask backend (machine learning model API) and a Streamlit frontend (user interface).

## Project Structure

- `backend/`: Contains the Flask application, model, and Dockerfile for the prediction service.
- `frontend/`: Contains the Streamlit application and Dockerfile for the user interface.
- `docker-compose.yml`: Orchestrates the backend and frontend services using Docker.

## Deployment with GitHub Codespaces

This application is designed for easy deployment using GitHub Codespaces. Follow these steps to get your application running:

1.  **Fork/Clone this Repository:** Get a copy of this repository.

2.  **Create a Codespace:**
    *   Go to your GitHub repository.
    *   Click the green "Code" button.
    *   Select the "Codespaces" tab.
    *   Click "Create codespace on `master`" (or your preferred branch).

3.  **Open Terminal:** Once the Codespace is ready, open a new terminal within the Codespace (Terminal > New Terminal).

4.  **Navigate to Deployment Directory:**
    ```bash
    cd deployment
    ```

5.  **Build and Run Docker Containers:** Execute the following command to build and run the Docker images for both your backend and frontend:
    ```bash
    docker-compose up --build -d
    ```

6.  **Access the Applications:**
    *   **Streamlit Frontend:** GitHub Codespaces will automatically detect and forward port `8501`. You should see a pop-up to open it in your browser. If not, check the "Ports" tab in the Codespace interface.
    *   **Flask Backend:** The Flask backend (port `8000`) is accessible internally by the Streamlit app using the service name `backend`.

## Local Development (Optional)

If you wish to run this application locally using Docker Compose:

1.  Ensure you have Docker and Docker Compose installed.
2.  Navigate to the `deployment` directory.
3.  Run `docker-compose up --build`.
4.  Access the Streamlit app at `http://localhost:8501`.
