from flask import Flask, render_template, request
import sys
import os
import json

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
        print(f"form_data:{form_data}")
        for k, v in form_data.items():
            print(f"(k, v):{(k, v)}")

        sys.path.append("MoonBoard")
        from MoonBoard.fetch_logbook import request_data

        # Get username and password
        username = form_data['username']
        password = form_data['password']
        # Define cache filename
        filename = f"logbook_{username}.json"

        # Download logbook, or fetch cached
        if not os.path.isfile(filename):
            # Download data and save
            logbook_data = request_data(access_kwargs={
                'username': username,
                'password': password})
            with open(filename, 'w') as json_file:
                json.dump(logbook_data, json_file, indent=4)
        else:
            # Load cached data
            with open(filename) as json_file:
                logbook_data = json.load(json_file)

        from run import construct_data
        # Load json data
        problems_2016_filename = 'MoonBoard/problems MoonBoard 2016 .json'
        with open(problems_2016_filename) as json_file:
            problem_data = json.load(json_file)

        data_dict = construct_data(problem_data, logbook_data)

        for k in data_dict.keys():
            print(f"k:{k}")

        from datahandlers.data import Logbook
        from datahandlers.data import DATAHANDLERS

        datahandlers = ['Logbook', 'Times']
        settings = {}
        general_kwargs = {'save': False}

        import base64
        import io
        from flask import Response
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from utils.html import frame, image, h2

        html = ""
        for datahandler in datahandlers:
            print(f"datahandler:{datahandler}")
            datahandler_class = DATAHANDLERS[datahandler]
            datahandler_obj = datahandler_class()

            # Extract possible settings kwargs from args.settings
            kwargs = settings[datahandler] if datahandler in settings else {}
            # Run datahandler object, with different inputs, and settings dict
            for k, v in data_dict.items():
                print(f"k:{k}")

            # fig, ax = datahandler_obj(**data_dict, save=False)
            fig, ax = datahandler_obj(**data_dict, save=False)
            print(f"fig, ax:{fig, ax}")
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            data = base64.b64encode(output.getbuffer()).decode("ascii")
            html += h2(datahandler)
            html += frame(image(data))

        return html


app.run(host='localhost', port=5000)
