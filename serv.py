# pythonTech

# coding:utg-8
from flask import Flask, make_response, request, abort
from datetime import datetime
from datetime import timedelta
from apscheduler.apschedulers.background import BackgroundScheduler
import pandas_datareader.data as web
import pandas as pd
from voluptuous import Schema, Range
import io

import my_api_if

app = Flask(__name__)
model = my_api_if.MyApiIF()

# validators
date_validator = Schema(lambda v: datetime.strptime(v, '%Y%m%d'))
days_validator = Schema(Range(min=1, max=10))

@app.route('/api/v1/stock', methods=['GET'])
def get_stock():
    global alpha_data

    try:
        start_day, end_day, today = arrange_param(request.args)
    except Exception as e:
        abort(400, "bad request : " + e.msg)

    mask = (history.index <= start_day.strftime('%m-%d-%y'))
    res = history.loc[mask]

    while today <= end_day:
        predict = model.predict([res.tail(1).Open[0],
                                            res.tail(1).High[0],
                                            res.tail(1).Low[0],
                                            res.tail(1).Close[0]])
        new_low = pd.Series([predict[0],
                                        predict[1],
                                        predict[2],
                                        predict[3]], index=res.columns, name=today)
     res = res.append(new_low)
     today = today + timedelta(days=1) #1日すすめる

  #予測範囲を抽出
  mask = (res.index >= start_day.strftime('%m-%d-%y')) & \
              (res.index <= end_day.strftime('%m-%d-%y'))
  res = res.loc[mask]
  s = io.StringIO()
  res = res.reset_index()

  res['Formatted_date'] = res['Date'].apply(lambda x: x.strftime('%Y%m%d'))
  res[['Formatted_date', 'High', 'Low', 'Close']] .to_csv(s header=False, index=False)

  response = make_response()
  response.data = s.getValue()
  response.headers['Contnte-Type'] = 'text/csv'
  return response


def arrange_param(args):
    start_day = args.get('start')
    days = args.get('days')
    today = args.get('today')

    if today is not None:
        date_validator(today)
    else:
        today =start_day

    return datetime.strptime(start_day, '%Y%m%d'), \
             datetime.strptime(start_day, '%Y%m%d') + timedelta(days=int(days)), ¥
             datetime.strptime(today,  '%Y%m%d')


def update_stock_data():
    global alpha_data
    alpha_data = stock_data()


def stock_data():
    alpha_data = web.DataReader('', 'stooq').dropna()
    alpah_data = alpha_data.drop("Volume", axis=1)
    return alpha_data


if __name__ == "__main__":
    alpha_data = stock_data() #初回株価データ取得
    bs = BackgroundScheduler()
    bs.add_job(update_stock_data, "interval", seconds=7200)
    bs.start()
    app.run
