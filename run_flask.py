import sys
import os
import json
import base64
import io

from flask import Flask, render_template, request
from run import construct_data
from datahandlers.data import DATAHANDLERS
from utils.html import frame, image, h2


app = Flask(__name__)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/data/', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form

        sys.path.append("MoonBoard")
        from MoonBoard.fetch_logbook import request_data

        # Get username and password
        username = form_data['username']
        password = form_data['password']
        # Define cache filename
        filename = f"logbook_{username}.json"

        # Download logbook, or fetch cached
        print(f"filename:{filename}")
        print(f"os.path.isfile(filename):{os.path.isfile(filename)}")
        # Download data and save
        logbook_data = request_data(access_kwargs={
            'username': username,
            'password': password})
        with open(filename, 'w') as json_file:
            json.dump(logbook_data, json_file, indent=4)

        # Load json data
        problems_2016_filename = 'MoonBoard/problems MoonBoard 2016 .json'
        with open(problems_2016_filename) as json_file:
            problem_data = json.load(json_file)

        data_dict = construct_data(problem_data, logbook_data)

        datahandlers = ['Logbook', 'Times']
        settings = {}
        general_kwargs = {'save': False}
        from utils.html import parse_docstring

        html = ""
        for datahandler in datahandlers:
            datahandler_class = DATAHANDLERS[datahandler]
            datahandler_obj = datahandler_class()

            # Extract possible settings kwargs from args.settings
            kwargs = settings[datahandler] if datahandler in settings else {}
            # Run datahandler object, with different inputs, and settings dict
            fig, ax = datahandler_obj(
                **{**data_dict, **general_kwargs, **kwargs})
            output = io.BytesIO()
            fig.savefig(output, format='png', bbox_inches="tight")
            data = base64.b64encode(output.getbuffer()).decode("ascii")

            docstr = parse_docstring(datahandler_obj)

            html += h2(datahandler)
            html += docstr
            html += frame(image(data))

        return html


app.run(host='localhost', port=5000)
