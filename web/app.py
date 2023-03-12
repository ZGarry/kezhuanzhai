import json
from flask import Flask, redirect, render_template, request, jsonify
from StrageyPool import StrageyPool
from Setting import Setting

# 生成flask容器
app = Flask(__name__)
strageyPool = StrageyPool(setting=Setting())


@app.route("/show")
def modeNameList():
    return json.dump(strageyPool.show())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/result.html")
def run():
    return render_template("result.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        name = request.form.get("name")
        mode = request.form.get("mode")
    if request.method == "GET":
        name = request.args.get("name")
        mode = request.args.get("mode")

    if len(name) == 0 or len(mode) == 0:
        return {'message': "error!"}
    else:
        # 生成对应mode-name下的对应内容
        strageyPool.add(mode, name)
        return {'message': "success!", 'name': name, 'mode': mode}


if __name__ == '__main__':
    # 启动flask
    # run里面是执行了run_simple（host,port，self=app,也就是flask对象）

    # 自动刷新
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run()
