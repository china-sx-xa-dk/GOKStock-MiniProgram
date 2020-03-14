import tushare as ts
import numpy as np
import pandas as pd
import os.path


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
        refresh_base_stock(_file_path)
    return pd.read_csv(_file_path)


# 每一列所有数据进行格式化,用于前台进行模糊匹配展示
def base_stock_one_row_list(root_path):
    _df = read_base_stock(root_path)
    _df['result'] = _df['ts_code'].map(lambda x: x[:6]) + ' ' + _df['area'].map(str) + ' ' + _df['name'].map(str)
    return _df['result'].values
