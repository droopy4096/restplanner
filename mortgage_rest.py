#!/bin/env python

from flask import Flask, jsonify
from mortgage.Mortgage import monthly_schedule, weekly_schedule
from datetime import date

app = Flask(__name__)


@app.route('/')
def index():
    return "PyMortgage API Endpoint"


@app.route('/schedule/monthly', methods=['GET'])
def get_monthly_schedule(year, month, day, years, step=1):
    schedule = monthly_schedule(date(year, month, day), years, step)
    return jsonify({'schedule': schedule})


@app.route('/schedule/weekly', methods=['GET'])
def get_weekly_schedule(year, month, day, years, step=1):
    schedule = weekly_schedule(date(year, month, day), years, step)
    return jsonify({'schedule': schedule})


if __name__ == '__main__':
    app.run(debug=True)
