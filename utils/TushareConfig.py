import tushare as ts


def get_tushare_pro():
    ts.set_token("988942bbd27a381710dd9840dfb06c6fb2be382cce6fd85a581f3f78")
    return ts.pro_api()


def add(x, y):
    return x+y


pass
