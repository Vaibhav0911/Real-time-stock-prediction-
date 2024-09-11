# backend/app.py
from flask import Flask, request, jsonify, render_template
import yfinance as yf
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
import plotly
import plotly.graph_objs as go
import json
import webbrowser  # Import the webbrowser module
from threading import Timer  # Use a timer to open the browser after the server starts

app = Flask(__name__)

# Load ML model and scaler
model = load_model('ml_model\stock_model.h5')
scaler = joblib.load('ml_model/scaler.save')


def fetch_stock_data(ticker, period='2y', interval='1d'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    data.reset_index(inplace=True)
    return data

def fetch_latest_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')  # Real-time data
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker']
    
    # Validate ticker
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400
    
    data = fetch_latest_data(ticker)
    if data.empty:
        return jsonify({'error': 'No data found for ticker'}), 400

    # Preprocess data
    last_60 = data['Close'].values[-60:]
    last_60_scaled = scaler.transform(last_60.reshape(-1, 1))
    X = np.array([last_60_scaled])
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Predict
    prediction = model.predict(X)
    predicted_price = scaler.inverse_transform(prediction)[0][0]
    
    # Convert the numpy.float32 to a Python float
    predicted_price = float(predicted_price)

    return jsonify({'predicted_price': predicted_price})

# backend/app.py
@app.route('/historical/<ticker>', methods=['GET'])
def get_historical_data(ticker):
    data = fetch_stock_data(ticker)
    if data.empty:
        return jsonify({'error': 'No data found for ticker'}), 400
    
    return jsonify({
        'dates': data['Date'].tolist(),
        'prices': data['Close'].tolist()
    })

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    
    Timer(2, open_browser).start()  # Delay the opening of the browser by 1 second
    app.run(debug=True)
