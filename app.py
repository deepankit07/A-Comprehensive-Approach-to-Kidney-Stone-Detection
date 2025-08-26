from flask import Flask, render_template, request
import joblib
import re
import pytesseract
import numpy as np
import os

app = Flask(__name__, static_url_path='/static')


model = joblib.load('vot_class.pkl')


keywords = {
    'gravity': r'Gravity\s*:\s*(\d+\.*\d*)',
    'urea': r'Urea\s*:\s*(\d+\.*\d*)',
    'osmolality': r'Osmolality\s*:\s*(\d+\.*\d*)',
    'conductivity': r'Conductivity\s*:\s*(\d+\.*\d*)',
    'pH': r'(?:REACTION\s*\(\s*PH\s*\))\s*[:=]\s*(\d+\.*\d*)',
    'calcium': r'Calcium\s*[:=]\s*(\d+\.*\d*)'
}

def extract_features_from_report(text):
    extracted_values = {}
    for keyword, pattern in keywords.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted_values[keyword] = float(match.group(1))
        else:
            extracted_values[keyword] = 3  
    feature_vector = np.array([[extracted_values[key] for key in ['gravity', 'pH', 'osmolality', 'conductivity', 'urea', 'calcium']]])
    return feature_vector



@app.route('/upload', methods=['POST'])
def upload():
    if 'report' not in request.files:
        return 'No file uploaded', 400

    report_file = request.files['report']
    if report_file.filename == '':
        return 'No file selected', 400
    
    report_text = pytesseract.image_to_string(report_file)
    print(report_text)

    
    feature_vector = extract_features_from_report(report_text)

    
    prediction = model.predict_proba(feature_vector)

    
    return f"Prediction probability for kidney stones (0: No, 1: Yes): {prediction[0][1]:.2f}"

if __name__ == '__main__':
    app.run(debug=True)