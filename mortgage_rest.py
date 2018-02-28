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
    print request.args
    n_req = dict(map(lambda x: (x[0], int(x[1])), request.args.items()))
    schedule = monthly_schedule(date(n_req['year'],
                                     n_req['month'],
                                     n_req['day']),
                                n_req['years'],
                                n_req.get('step', 1))
    return jsonify({'schedule': schedule2json(schedule)})


@app.route('/schedule/weekly', methods=['GET'])
def get_weekly_schedule(year, month, day, years, step=1):
    n_req = dict(map(lambda x: (x[0], int(x[1])), request.args.items()))
    schedule = weekly_schedule(date(n_req['year'],
                                    n_req['month'],
                                    n_req['day']),
                               n_req['years'],
                               n_req.get('step', 1))
    return jsonify({'schedule': schedule})


if __name__ == '__main__':
    app.run(debug=True)
