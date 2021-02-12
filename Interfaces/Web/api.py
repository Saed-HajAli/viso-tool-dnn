import os

from flask import Blueprint
import json
from flask import Flask, flash, request, redirect, url_for, render_template, json,jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import uuid


Api = Blueprint('Api', __name__)


@Api.route('/create_job', methods=['POST'])
def create_dataset():

    jsondata = [json.loads(obj) for obj in request.json]

    id = uuid.uuid4().hex[:8]

    file_name = str(id)
    # os.makedirs('static/data/' + folder_name)

    with open('static/data/' + file_name + '.json', 'w') as f:
        json.dump(jsondata, f)

    reques_url = url_for('run',id=file_name,_external=True)

    return reques_url


