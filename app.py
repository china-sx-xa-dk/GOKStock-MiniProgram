from flask import Flask,make_response, jsonify
from flask_apscheduler import APScheduler


# 配置定时任务
class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        # {  # 第一个任务
        #     'id': 'job1',
        #     'func': '__main__:job_1',
        #     'args': (1, 2),
        #     'trigger': 'cron', # cron表示定时任务
        #     'hour': 19,
        #     'minute': 27
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


# 获取股票列表
# 获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
@app.route('/getBasicStock')
def basic_stock():
    response = make_response(jsonify({'test': 'good'}, 403))
    return response


if __name__ == '__main__':
    # 定时器
    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    app.run(debug=True, port=8080)
