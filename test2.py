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
        datahandler = Logbook()
        fig, ax = datahandler(**data_dict, save=False)
        import io
        from flask import Response
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)

        import base64
        data = base64.b64encode(output.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"

        # return Response(output.getvalue(), mimetype='image/png')
        # return render_template('data.html', form_data=form_data)


app.run(host='localhost', port=5000)
