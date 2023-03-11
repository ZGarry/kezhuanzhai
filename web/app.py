from flask import Flask, redirect, render_template

from Backtesting import Backtesting

# 生成flask容器
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/currentMode")
def currentMode():
    # 当前模式
    return render_template("result.html")


# 放到templates文件夹可使用
@app.route("/run")
def run():
    # 分为一个两阶段步骤，第一步，录入一些参数
    # 第二部，展示新内容

    # Backtesting().run()
    return render_template("result.html")


if __name__ == '__main__':
    # 启动flask
    # run里面是执行了run_simple（host,port，self=app,也就是flask对象）
    app.run()
