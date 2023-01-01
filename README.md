# moonboard-plots


## Setup
Install python dependencies via
```
python -m pip install flask
python -m pip install pygame
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

For the moment, add pull request to enable 2016 holds and fetching of the logbook
```
git fetch origin pull/2/head:other_holdsets
git fetch origin pull/3/head:fetch_logbook

git co fetch_logbook 
git rebase other_holdsets 
```

Edit secret.py with username and password

Fetch problems
```
python fetch_problems.py 
```

## Generate output
The idea is having one main script for loading the data, and some modular system for different plots, statistics or other. The main script is 'run.py'. It loads data and pass this to some 'datahandlers'.

Currently there is a focus on the 2016 Moonboard setup. All problem data are loaded from a .json file, resulting in a list of 'problem-dicts'. Data is passed to the datahandlers in this 'raw' form, but also reformatted using some simple 'Problem' and 'Move' classes. The latter allows accessing data as attributes (e.g. problem.isBenchmark) instead of as (nested) dicts (problem['isBenchmark']).

The following command will run two datahandlers. The first will produce a 'problem view' for all benchmark problems (by default in the Output/Benchmarks folder), and the second will produce a visualization which holds are used the most for each grade among the benchmarks (by default in the Output/BenchmarkHoldFrequency folder).
```
python run.py --datahandlers Benchmarks BenchmarkHoldFrequency
```

## Settings
run.py takes some arguments. `--filename` is the path to the dataset file, by default 'MoonBoard/problems MoonBoard 2016 .json'. `--save-dir` is the folder where to save data, by default 'Output'. `--datahandlers` take one or several datahandlers, as seen above. Using `--settings` one can provide arguments to the datahandlers. These can be general or specific. General settings are provided as e.g. `--settings overwrite:True` and will be given to all datahandlers. Specific settings are provided as e.g. `--settings BenchmarkHoldFrequency:"dict(overwrite=True)"` and will only apply to the specified datahandler.

Datahandlers can return data in the form of dicts, and which is then passed to following datahandlers. If someone e.g. developed a 'generate Moonboard beta' algorithm, this could be implemented as a datahandler, and then used by other datahandlers.
