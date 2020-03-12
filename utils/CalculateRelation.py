import matplotlib.pyplot as plt  # 提供类matlab里绘图框架
import numpy as np
import pandas as pd
import tushare as ts

# 获取数据

s_md = '000333.SZ'  # 美的
s_gl = '000651.SZ'  # 格力
sdate = '2016-04-25'  # 起止日期
edate = '2019-04-25'

ts.set_token("988942bbd27a381710dd9840dfb06c6fb2be382cce6fd85a581f3f78")
pro = ts.pro_api()

df_md = pro.daily(ts_code=str(s_md), start_date=str(sdate), end_date=str(edate))
df_gl = pro.daily(ts_code=str(s_gl), start_date=str(sdate), end_date=str(edate))
df = pd.concat([df_md.trade_date, df_md.close, df_gl.close], axis=1, keys=['trade_date', 'md_close', 'gl_close'])  # 合并
df.ffill(axis=0, inplace=True)  # 填充缺失数据
df.to_csv('md_gl.csv')

# pearson方法计算相关性
corr = df.corr(method='pearson', min_periods=1)
print(corr)

# 打印图像
df.plot(figsize=(20, 12))
plt.savefig('md_gl.png')
plt.close()

# 归一化处理打印图像
df['md_one'] = df.md_close / float(df.md_close[0]) * 100
df['gl_one'] = df.gl_close / float(df.gl_close[0]) * 100
df.md_one.plot(figsize=(20, 12))
df.gl_one.plot(figsize=(20, 12))
plt.savefig('md_gl_one.png')