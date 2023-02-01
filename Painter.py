# from . import Painter
import pyecharts.options as opts
from pyecharts.charts import Line


class Painter:
    def __init__(self, backtesterList):
        self.backtesterList = backtesterList #回测集合
    
    def paint(self):

        """
        Gallery 使用 pyecharts 1.1.0
        参考地址: https://echarts.apache.org/examples/editor.html?c=line-smooth

        目前无法实现的功能:

        暂无
        """
        # 获取最大长度，必须确保时间是同一尺度才有意义
        max_len = max(map(lambda x: len(x.posValueList),self.backtesterList))

        x_data = list(range(max_len))


        C = (
            Line()
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
            .add_xaxis(xaxis_data=x_data)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="可转债历史所有数据分析"),
                xaxis_opts=opts.AxisOpts(
                                        name='日期/天',
                                        min_interval=100,
                                        splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(rotate=45),
                                        ),
            yaxis_opts=opts.AxisOpts(name='资金',
                    splitline_opts=opts.SplitLineOpts(is_show=True),))
        )

        for backtester in self.backtesterList:
            C =(C.add_yaxis(
                    series_name=backtester.mode,
                    y_axis=backtester.posValueList,
                    symbol="emptyCircle",
                    is_symbol_show=True,
                    is_smooth=True,
                    label_opts=opts.LabelOpts(is_show=False),
                    linestyle_opts=opts.LineStyleOpts(width=1,color='rgb(255, 0, 0)'),
                ))
        C = (C.render("build/result.html"))