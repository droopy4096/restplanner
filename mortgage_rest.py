#!/bin/env python

from flask import Flask, jsonify, request
from mortgage.TermScheduler import monthly_schedule, weekly_schedule, schedule2json
from datetime import date

app = Flask(__name__)


@app.route('/')
def index():
    return "PyMortgage API Endpoint"


@app.route('/schedule/monthly', methods=['GET'])
# def get_monthly_schedule(year, month, day, years, step=1):
def get_monthly_schedule():
    schedule = monthly_schedule(date(int(request.args['year']),
                                     int(request.args['month']),
                                     int(request.args['day'])),
                                int(request.args['years']),
                                int(request.args.get('step', 1)))
    return jsonify({'schedule': schedule2json(schedule)})


@app.route('/schedule/weekly', methods=['GET'])
def get_weekly_schedule(year, month, day, years, step=1):
    schedule = weekly_schedule(date(year, month, day), years, step)
    return jsonify({'schedule': schedule})


if __name__ == '__main__':
    app.run(debug=True)
