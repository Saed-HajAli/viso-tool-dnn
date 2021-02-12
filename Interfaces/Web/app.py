import os
import json
from os.path import join, dirname, realpath
from flask import Flask, flash, request, redirect, url_for, render_template, json,jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from Interfaces.Web.api import Api
from VisPackage.Viso import Epoch
from collections import namedtuple

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.register_blueprint(Api, url_prefix='/api')
app.register_blueprint(Api)



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/read')
def read():
    for idx, val in enumerate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20]):
        pd.DataFrame(pd.read_csv("../../static/data/out.csv", sep=",", header=0, index_col=False)) \
            .to_json("../../static/data/mnist/out.json", orient="records", date_format="epoch", double_precision=10,
                     force_ascii=True, date_unit="ms", default_handler=None)
    return "Done!"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))


@app.route('/vis', methods=['GET'])
def view_data():

    if 'data' not in request.args:
        return "Set Data Value in URL [mnist | cifar] !"

    dataset = {
        "mnist": 20,
        "cifar": 196,
    }

    full_data = []
    for i in range(1, int(request.args.get("epoch")) + 1):
        full_data.append(json.load(open("static/data/" + request.args.get("data") + "/cifar_" + str(i) + ".json")))

    with open('static/data/' + 'cifar' + '.json', 'w') as f:
        json.dump(full_data, f)

    return render_template('index.html', data=json.dumps(full_data))


@app.route('/run', methods=['GET','POST'])
def run():
    full_data = json.load(open("static/data/" + request.args['id'] + ".json"))

    Settings = Epoch.Settings()
    view = True
    if request.json is not None:
        config = json.loads(json.dumps(request.json), object_hook=lambda d: namedtuple('Settings', d.keys(), module=Epoch.Settings)(*d.values()))
        Settings.probtpFilter = config.Settings.probtpFilter
        Settings.probbins = config.Settings.probbins
        Settings.probLimits = config.Settings.probLimits
        Settings.probtnFilter = config.Settings.probtnFilter
        Settings.boxIQR = config.Settings.boxIQR
        view = False

    model = Epoch(full_data[0], Settings)

    if view:
        return render_template('index.html', data=json.dumps(model.getDataJson()))
    else:
        return json.dumps(model.getDataJson())


@app.route('/test', methods=['GET'])
def test():
    full_data = json.load(open("../../static/data/out.json"))
    m = Epoch(full_data[0])

    return jsonify(m.getDataJson())




if __name__ == '__main__':
    app.run()
