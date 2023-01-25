import sys
import os
import json
import base64
import io

from flask import Flask, render_template, request
from run import construct_data
from datahandlers.data import DATAHANDLERS
from utils.html import frame, image, h2, h4


app = Flask(__name__)


@app.route('/')
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/example')
def example():
    return render_template('example.html')


@app.route('/example2')
def example2():
    return render_template('example2.html')


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
        try:
            logbook_data = request_data(access_kwargs={
                'username': username,
                'password': password})
        except KeyError:
            from utils.html import get_wrong_password_string
            html = h2(get_wrong_password_string())
            html += "Your probably entered the wrong username or password"

            return html

        with open(filename, 'w') as json_file:
            json.dump(logbook_data, json_file, indent=4)

        data_dict = construct_data(
            logbook_data=logbook_data, problem_data=None)

        datahandlers = [
            'BenchmarkProgress', 'BenchmarkProgressPerGrade',
            'Times',
        ]
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
            datahandler_output = datahandler_obj(
                **{**data_dict, **general_kwargs, **kwargs})

            docstr = parse_docstring(datahandler_obj)

            html += h2(datahandler)
            html += docstr

            if type(datahandler_output) == tuple:
                fig, ax = datahandler_output
                output = io.BytesIO()
                fig.savefig(output, format='png', bbox_inches="tight")
                data = base64.b64encode(output.getbuffer()).decode("ascii")
                html += frame(image(data))
            elif type(datahandler_output) == dict:
                for name, (fig, ax) in datahandler_output.items():
                    output = io.BytesIO()
                    fig.savefig(output, format='png', bbox_inches="tight")
                    data = base64.b64encode(output.getbuffer()).decode("ascii")
                    html += h4(name)
                    html += frame(image(data))

        return html


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
