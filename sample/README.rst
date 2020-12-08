Sample use
==========

Fetch schedule
--------------

manually::

  curl 'https://restplanner-200203.appspot.com/schedule/monthly?year=2010&month=2&day=1&years=15&step=1' > monthly_schedule_15_1.json

setup mortgage
--------------

manually::

  cat > mortgage.json
  {
    "house_price": 300000,
    "interest": 0.04,
    "downpayment": 5000,
    "schedule": {}
  }
  ^D

merge mortgage & schedule setup info
------------------------------------

manually::

  jq -s '.[0] * .[1]' monthly_schedule_15_1.json mortgage.json > mortgage_setup.json

Generate payment table
-----------------------

manually::

  curl -X POST -H "Content-Type: application/json" --data @mortgage_setup.json https://restplanner-200203.appspot.com/mortgage > payment_schedule.json

Assemble ROI request object
---------------------------

manually::

  jq -s '.[0] * .[1] * .[2] * .[3]' monthly_schedule_15_1.json mortgage.json payment_schedule.json roi_setup.json > roi_request.json

Request ROI table
-----------------

manually::

  curl -X POST -H "Content-Type: application/json" --data @roi_request.json http://restplanner-200203.appspot.com/roi > roi.json
