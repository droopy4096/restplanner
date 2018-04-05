#!/bin/env python

from flask import Flask, jsonify, request, abort
from mortgage.TermScheduler import monthly_schedule, weekly_schedule
from mortgage.TermScheduler import schedule2json, json2schedule
from mortgage.Mortgage import Mortgage
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
def get_weekly_schedule():
    n_req = dict(map(lambda x: (x[0], int(x[1])), request.args.items()))
    schedule = weekly_schedule(date(n_req['year'],
                                    n_req['month'],
                                    n_req['day']),
                               n_req['years'],
                               n_req.get('step', 1))
    return jsonify({'schedule': schedule})


@app.route('/mortgage', methods=['POST'])
def get_mortgage():
    # Mortgage(300000, 0.035, 300000 * 0.2, monthly_schedule(date(2009, 10, 1), 15))
    if not request.json:
        abort(400)
    house_price = float(request.json['house_price'])
    interest = float(request.json['interest'])
    downpayment = float(request.json['downpayment'])
    schedule = json2schedule(request.json['schedule'])
    m = Mortgage(house_price, interest, downpayment, schedule)
    payments = []
    for s in m.payments():
        payments.append(s.serialize_json())

    return jsonify(payments)


if __name__ == '__main__':
    app.run(debug=True)
