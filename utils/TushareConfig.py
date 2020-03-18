#! /usr/bin/env python3
# encoding: utf-8
import tushare as ts
import numpy as np
import pandas as pd
import os.path
from io import BytesIO
import base64
import matplotlib.pyplot as plt  # 提供类matlab里绘图框架
from flask import jsonify


# 获取有Token的Tushare接口访问对象
ts.set_token("988942bbd27a381710dd9840dfb06c6fb2be382cce6fd85a581f3f78")
pro = ts.pro_api()


# 刷新股票列表
def refresh_base_stock(file_path):
    pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date').to_csv(file_path)


# 读取DataFrame原型数据
def read_base_stock(root_path):
    _path = root_path+'/csv'
    _file_path = _path + '/stock_basic.csv'
    # 去除首尾空格
    _path = _path.strip().rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    _is_exists = os.path.exists(_path)
    # 判断结果
    if not _is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(_path)
        # 初次创建目录后主动刷新股票列表获取数据 否则无法读取
        refresh_base_stock(_file_path)
    # 读取股票列表数据
    return pd.read_csv(_file_path)


# 每一列所有数据进行格式化,用于前台进行模糊匹配展示
# 格式化后的数据格式为:股票代码 股票地址 股票名称
def base_stock_one_row_list(root_path):
    _df = read_base_stock(root_path)
    _df['result'] = _df['ts_code'].map(lambda x: x[:6]) + ' ' + _df['area'].map(str) + ' ' + _df['name'].map(str)
    return _df['result'].values


# 获取数据
# 两个时间段 开始时间 结束时间
# 两只股票的代码
def calculate_relation(_stock_start_data
                       , _stock_end_data
                       , _first_stock_code
                       , _second_stock_code
                       , _first_show_code
                       , _second_show_code
                       , _first_show_name
                       , _second_show_name
                       ):
    # 通过接口获取时间段内每一天的收盘价
    _df_first_stock = pro.daily(ts_code=str(_first_stock_code), start_date=str(_stock_start_data), end_date=str(_stock_end_data))
    print(_df_first_stock)
    _df_second_stock = pro.daily(ts_code=str(_second_stock_code), start_date=str(_stock_start_data), end_date=str(_stock_end_data))
    print(_df_second_stock)
    df = pd.concat([_df_first_stock.trade_date, _df_first_stock.close, _df_second_stock.close], axis=1, keys=['trade_date', _first_show_code, _second_show_code])  # 合并
    df.ffill(axis=0, inplace=True)  # 填充缺失数据
    # df.to_csv('md_gl.csv')    # 保存数据到.csv文件
    # pearson方法计算相关性
    corr = df.corr(method='pearson', min_periods=1)
    print(corr)
    if corr[_first_show_code][_first_show_code] == 1:
        relation_result = corr.loc[_first_show_code][_second_show_code]
    else:
        relation_result = corr.loc[_first_show_code][_first_show_code]
    # 设置图像为600,650的像素
    df.plot(figsize=(6, 6.5))
    # plt.savefig('md_gl.png')  # 保存图像
    # 写入内存
    save_file = BytesIO()
    plt.savefig(save_file, format='png')
    # 转换base64并以utf8格式输出
    save_file_base64 = base64.b64encode(save_file.getvalue()).decode('utf8')
    plt.close()
    # 构建json数据
    return jsonify({'first_code': _first_show_code, 'second_code': _second_show_code, 'first_name': _first_show_name, 'second_name': _second_show_name, 'relation_result': relation_result, 'base64': save_file_base64, 'start_data': _stock_start_data, 'end_data': _stock_end_data})

