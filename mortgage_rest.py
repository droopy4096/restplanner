#!/bin/env python

from flask import Flask, jsonify, request, abort
from mortgage.TermScheduler import monthly_schedule, weekly_schedule
from mortgage.TermScheduler import schedule2json, json2schedule
from mortgage.Mortgage import Mortgage, RapidPayMortgage
from mortgage.MortgageStatement import mortgagestatement2json, json2mortgagestatement
from mortgage.ROI import ROI
from datetime import date

app = Flask(__name__)

class MortgageWrapper(Mortgage):
    def __init__(self,json_data):
        """Fake mortgage oobject for unwrapping pre-calculated JSON:
        {
            "house_price": 100000,
            "interest":  0.025,
            "downpayment": 1000,
            "schedule": {
                "annual_periods": 12, 
                "start_date": "2020-02-01", 
                "end_date": "2025-02-01", 
                "events": [
                    "2010-02-01", 
                    ...
                ]
            },
            "payments": [ ... ]
        }
        """
        house_price=float(json_data['house_price'])
        interest=float(json_data['interest'])
        downpayment=float(json_data['downpayment'])
        # schedule=json_data['schedule']
        schedule = json2schedule(json_data['schedule'])
        Mortgage.__init__(self, house_price, interest, downpayment, schedule)
        self._payments=[]
        for p in json_data['payments']:
            self._payments.append(json2mortgagestatement(p))

    def payments(self):
        return self._payments

@app.route('/')
def index():
    return "PyMortgage API Endpoint"


@app.route('/schedule/monthly', methods=['GET'])
# def get_monthly_schedule(year, month, day, years, step=1):
def get_monthly_schedule():
    # print request.args
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

    return jsonify({'payments': payments})

# TODO Need to finalize prepayment schedule machinery
@app.route('/rapidmortgage', methods=['POST'])
def get_rapidmortgage():
    # Mortgage(300000, 0.035, 300000 * 0.2, monthly_schedule(date(2009, 10, 1), 15))
    if not request.json:
        abort(400)
    house_price = float(request.json['house_price'])
    interest = float(request.json['interest'])
    downpayment = float(request.json['downpayment'])
    schedule = json2schedule(request.json['schedule'])
    prepay_schedule = json2schedule(request.json['prepay_schedule'])
    m = RapidPayMortgage(house_price, interest, downpayment, schedule, prepay_schedule)
    payments = []
    for s in m.payments():
        payments.append(s.serialize_json())

    return jsonify(payments)

@app.route('/roi', methods=['POST'])
def get_roi():
    if not request.json:
        abort(400)
    # mortgage_json = request.json['mortgage']
    mortgage_json = request.json
    target_sell_price = float(request.json['target_sell_price'])
    appreciation = float(request.json['appreciation'])
    baseline_return = float(request.json['baseline_return'])
    investments = float(request.json['investments'])
    property_tax_rate = float(request.json['property_tax_rate'])
    property_insurance = float(request.json['property_insurance'])
    tax_rate = float(request.json['tax_rate'])
    sale_expences = float(request.json['sale_expences'])

    mortgage=MortgageWrapper(mortgage_json)
    roi=ROI( mortgage=mortgage, 
            target_sell_price=target_sell_price, 
            appreciation=appreciation, 
            baseline_return=baseline_return, 
            investments=investments, 
            property_tax_rate=property_tax_rate, 
            property_insurance=property_insurance, 
            tax_rate=tax_rate, 
            sale_expences=sale_expences)
    roi_list=[]
    for r in roi():
        roi_list.append(r.serialize_json())

    return jsonify(roi_list)


if __name__ == '__main__':
    app.run(debug=True)
