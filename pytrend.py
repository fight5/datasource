from flask import Flask, jsonify, render_template, request
from pytrends.request import TrendReq
import pandas as pd
import time

app = Flask(__name__)

pytrends = TrendReq(hl='en-US', tz=360)

def get_trend_data(keywords, timeframe='today 3-m'):
    for _ in range(3):  # Try up to 3 times
        try:
            pytrends.build_payload(kw_list=keywords, timeframe=timeframe)
            df = pytrends.interest_over_time()
            return df
        except Exception as e:
            if "429" in str(e):  # If it's a rate limit issue
                time.sleep(10)  # Wait for 10 seconds before retrying
            else:
                raise e
    return None

@app.route('/')
def index():
    return render_template('chart.html')

@app.route('/get_data')
def get_data():
    # Get keywords from request parameters
    keywords = request.args.getlist('keywords') or ["football", "rugby"]
    
    df = get_trend_data(keywords)
    
    if df is None:
        return jsonify({"error": "Google Trends API rate limit reached."}), 429

    datasets = []
    for keyword in keywords:
        datasets.append({
            "label": keyword,
            "data": df[keyword].tolist(),
            "fill": False,
            "borderColor": "rgb(75, 192, 192)",
        })

    return jsonify({
        "dates": df.index.strftime('%Y-%m-%d').tolist(),
        "datasets": datasets
    })

if __name__ == "__main__":
    app.run(debug=True)

