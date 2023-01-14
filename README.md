# moonboard-plots
A repository for creating visualization of Moonboard data.
There is also a page which can generate some selected figures, https://www.moonplt.com/

## Setup
Install python dependencies via
```
python -m pip install matplotlib
python -m pip install numpy
python -m pip install flask
python -m pip install colorcet
python -m pip install requests
```
Download submodule, https://github.com/spookykat/MoonBoard via
```
git submodule update --init
```
Move into MoonBoard folder,
```
cd MoonBoard
```

For the moment, add pull request to enable fetching the logbook
```
git fetch origin pull/3/head:fetch_logbook

git checkout fetch_logbook 
git rebase main
```

Edit secret.py with username and password

Fetch problems, this might take a minute or two.
```
python fetch_problems.py 
```
Fetch logbook, this will probably not takes as long.
```
python fetch_logbook.py 
```

## Generate output
The idea is having one main script for loading the data, and some modular system for different plots, statistics or other. The main script is 'run.py'. It loads data and pass this to some 'datahandlers'.

The following command will run two datahandlers. The first will produce a 'benchmark progress plot', showing the accumulated number of benchmarks as a function of time for some logbook, for all used holdsets and angles. The second will produce a scatter plot showing what week days and time benchmarks have been registered (sent?), for some logbook.
```
python run.py --datahandlers BenchmarkProgress Times
```

Another example would be 
```
python run.py --datahandlers Benchmarks BenchmarkHoldFrequency
```
The first will produce a 'problem view' for all benchmark problems of the chosen dataset file (by default in the Output/Benchmarks folder), and the second will produce a visualization which holds are used the most for each grade among the benchmarks (by default in the Output/BenchmarkHoldFrequency folder).

## Settings
run.py takes some arguments. `--filename` is the path to the dataset file, by default 'MoonBoard/problems MoonBoard 2016 .json'. `--save-dir` is the folder where to save data, by default 'Output'. `--datahandlers` take one or several datahandlers, as seen above. Using `--settings` one can provide arguments to the datahandlers. These can be general or specific. General settings are provided as e.g. `--settings overwrite:True` and will be given to all datahandlers. Specific settings are provided as e.g. `--settings BenchmarkHoldFrequency:"dict(overwrite=True)"` and will only apply to the specified datahandler.

Datahandlers can return data in the form of dicts, and which is then passed to following datahandlers. If someone e.g. developed a 'generate Moonboard beta' algorithm, this could be implemented as a datahandler, and then used by other datahandlers.


## Run the web service
The web interface can be started by running
```
python run_flask.py
```
which will start a server listening on `localhost:5000`. As it will inform, this is a development server not to be used in deployment. One can anyway make it reachable from outside by instead running
```
flask --app run_flask.py run --host=0.0.0.0
```
This might be useful for trying a mobile interface e.g.

## How can I contribute?
Contributions are appreciated! Examples could be
- ideas for plots
- implementation of plots
- web design (...)


