
import os
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line
from datetime import  datetime



def convert_time(x):
    return str(x).replace(' 00:00:00','')
from datetime import datetime
name = datetime.now().strftime('%Y%m%d')

ROOT=r'C:\data'
filename = '2021-10-23 11_03_59.084803低溢价.xlsx'
df = pd.read_excel(os.path.join(ROOT,filename))

filename2='2021-10-23 11_02_39.614603双低.xlsx'
df2 = pd.read_excel(os.path.join(ROOT,filename2))

filename3='2021-10-23 10_59_06.193441低价.xlsx'
df3 = pd.read_excel(os.path.join(ROOT,filename3))


X=df.index.tolist()
X=list(map(convert_time,X))
Y=df['收益率'].map(lambda x:round(x,0)).tolist()
Y2=df2['收益率'].map(lambda x:round(x,0)).tolist()
Y3=df3['收益率'].map(lambda x:round(x,0)).tolist()
title="低溢价"
title2="双低"
title3='低价'

full_title = '低溢价，双低，低价[10只，5天轮]'
full_title1 = '低溢价，双低，低价收益率【10只，5天轮动】'

types=full_title1
y_min = min(min(Y),min(Y2))
y_max = max(max(Y),max(Y2))

c = (
    Line()
    .add_xaxis(X)
    .add_yaxis(title, Y, is_smooth=True,
    label_opts=opts.LabelOpts(is_show=False),
linestyle_opts=opts.LineStyleOpts(width=2,color='rgb(255, 0, 0)'),
    ).add_yaxis(title2, Y2, is_smooth=True,
linestyle_opts=opts.LineStyleOpts(width=2,color='rgb(0, 0, 255)'),
label_opts=opts.LabelOpts(is_show=False),
    ).add_yaxis(title3, Y3, is_smooth=True,
linestyle_opts=opts.LineStyleOpts(width=2,color='rgb(0, 255, 0)'),
label_opts=opts.LabelOpts(is_show=False),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title=full_title),
        xaxis_opts=opts.AxisOpts(
                                name='日期',
                                min_interval=100,
                                splitline_opts=opts.SplitLineOpts(is_show=True),
           axislabel_opts=opts.LabelOpts(rotate=45),
                                ),
        yaxis_opts=opts.AxisOpts(name='收益率%',
                                interval=5,
                                 min_=y_min-5,
                                 max_=y_max+5,
            splitline_opts=opts.SplitLineOpts(is_show=True),
        )
                                    )
                                    .set_colors(['red','blue','green']) # 点的颜色
    .render(f"多曲线plot_line_{name}_{types}.html")
)