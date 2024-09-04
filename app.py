from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the app
CORS(app)

# Load the trained model
model_path = r"C:\\Users\\ASUS\\project\\Anemia Detection\\random_forest_model(2).pkl"  # Path to your trained model
model = pickle.load(open(model_path, 'rb'))

# Define the function to preprocess input data
def preprocess_data(hemoglobin, gender, mcv):
    # Convert gender to numeric value
    gender_mapping = {'Male': 0, 'Female': 1}
    gender = gender_mapping.get(gender, 0)  # Default to 0 if gender is not found

    # Ensure non-negative values for hemoglobin and MCV
    hemoglobin = max(hemoglobin, 0)
    mcv = max(mcv, 0)

    # Create a dataframe with the input data
    data = {'Gender': [gender], 'Hemoglobin': [hemoglobin], 'MCV': [mcv]}
    df = pd.DataFrame(data)

    return df

# Define the function to predict anemia
def predict_anemia(hemoglobin, gender, mcv):
    # Preprocess the input data
    df = preprocess_data(hemoglobin, gender, mcv)

    # Predict anemia using the trained model
    prediction = model.predict(df)

    # Return the prediction
    return prediction[0]

# Define the route for the prediction API
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.get_json(force=True)
    hemoglobin = data['hemoglobin']
    gender = data['gender']
    mcv = data['mcv']

    # Call the predict_anemia function
    prediction = predict_anemia(hemoglobin, gender, mcv)

    # Return the prediction as a JSON response
    return jsonify({'prediction': int(prediction)})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
