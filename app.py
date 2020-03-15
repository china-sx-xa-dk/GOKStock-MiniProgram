#! /usr/bin/env python3
#encoding: utf-8
import os
from flask import Flask,make_response, jsonify
from flask_apscheduler import APScheduler
from TushareConfig import base_stock_one_row_list, calculate_relation, read_base_stock
import datetime


# 配置定时任务
class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        # {  # 第一个任务
        # 'id': 'job1',
        # 'func': '__main__:job_1',
        # 'args': (1, 2),
        # 'trigger': 'cron', # cron表示定时任务
        # 'hour': 19,
        # 'minute': 27
        # },
        {  # 第二个任务，每隔5S执行一次
            'id': 'job2',
            'func': '__main__:method_test',  # 方法名
            'args': (1, 2),  # 入参
            'trigger': 'interval',  # interval表示循环任务
            'seconds': 5,
        }
    ]


def method_test(a, b):
    print(a + b)


app = Flask(__name__)
app.config.from_object(Config())  # 为实例化的flask引入配置


# 获取股票列表,用于前端模糊匹配
# demo:http://127.0.0.1:8080/getBasicStock
@app.route('/getBasicStock', methods=['POST'])
def get_basic_stock():
    data = base_stock_one_row_list(os.path.dirname(app.instance_path).replace('\\', '/'))
    response = make_response(jsonify({'CodeStatus': 200, 'BasicStockOneRowList': data.tolist()}))
    return response


# 计算相关性
# 返回CalculateRelaionResultClass对象结构
# params1 _first_stock:第一支股票的代码
# params2 _second_stock:第二支股票的代码
# params3 _time_type a = '一个月',b = '三个月',c = '一年',d = '三年'
# demo:http://127.0.0.1:8080/getCalculateRelationResult/000001/000002/c
@app.route('/getCalculateRelationResult/<_first_stock>/<_second_stock>/<any(a,b,c,d):_time_type>', methods=['POST'])
def get_calculate_relation_result(_first_stock, _second_stock, _time_type):
    # tushare的唯一标识比股票代码多加.SZ
    _first_tushare_stock_code = _first_stock + '.SZ'
    _second_tushare_stock_code = _second_stock + '.SZ'

    # 通过_time_type计算需要提前多少天进行计算
    _day_cut = int
    if _time_type == 'a':
        _day_cut = -30
    elif _time_type == 'b':
        _day_cut = -90
    elif _time_type == 'c':
        _day_cut = -365
    else:
        _day_cut = -1095

    # 计算用户选择后的日期
    _now_time = datetime.datetime.now()
    _end_time = _now_time.strftime('%Y-%m-%d')    # 结束日期
    # 选择要提前的天数
    _calculate_time = _now_time + datetime.timedelta(days=_day_cut)
    _start_time = _calculate_time.strftime('%Y-%m-%d')    # 开始日期
    # 获取股票列表查询到股票的名称
    _data = read_base_stock(os.path.dirname(app.instance_path).replace('\\', '/'))
    _first_stock_name = _data[_data.ts_code == _first_tushare_stock_code].name[0]
    _second_stock_name = _data[_data.ts_code == _second_tushare_stock_code].name[1]
    # 进行两只股票的相关型和绘图
    return_data = calculate_relation(_start_time, _end_time, _first_tushare_stock_code, _second_tushare_stock_code, _first_stock, _second_stock, _first_stock_name, _second_stock_name)
    return make_response(return_data)


if __name__ == '__main__':
    # 定时器
    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    app.run(debug=True, port=8080)
