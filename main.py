from flask import Flask, render_template, request, jsonify
import logging
import requests
import numpy as np
import pandas as pd
import os

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import OrderBy

## Set up global variables

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'Quickstart-7994e573f0e9.json'
property_id = '407450748'

client = BetaAnalyticsDataClient()
app = Flask(__name__)

@app.route("/")
def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-WVSS9PG2CJ"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-WVSS9PG2CJ');
    </script>
    """
    # Create buttons to access functions
    buttons = """
    <a href="/logger"><button>Logger Function</button></a>
    <a href="/get_google_cookies"><button>Get Google Cookies</button></a>
    <a href="/response"><button>Google Analytics Response</button></a>
    """

    return prefix_google + "Hello                 " + buttons

@app.route('/logger')
def logger():
    # Log a message in the Python console
    logging.info("This is a Python log message.")

    # Log a message in the browser's console
    print("console.log('This is a browser log message.');")

    # Add a message to be displayed in a textbox on the page
    message = "This message will appear in a textbox on the page."

    return message

@app.route('/get_google_cookies')
def get_google_cookies():
    # Send a GET request to Google and retrieve the cookies
    response = requests.get("https://www.google.com/")
    cookies = response.cookies.get_dict()

    return jsonify(cookies)

@app.route('/response')
def response():
    # Replace this URL with your Google Analytics URL
    url = "https://analytics.google.com/analytics/web/#/p407450748/reports/reportinghub"
    # Send a GET request to the Google Analytics URL
    req = requests.get(url)

    return req.text

if __name__ == '__main__':
    app.run(debug=True)


