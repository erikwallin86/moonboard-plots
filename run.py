import json
import argparse
import os

from datahandlers.data import DATAHANDLERS
from utils.utils import StoreDict
from utils.utils import Problem

parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='Path to dataset files', nargs='*',
                    default='MoonBoard/problems MoonBoard 2016 .json')
parser.add_argument('--save-dir', type=str, default='Output',
                    help='where to save data')
parser.add_argument(
    '--datahandlers', type=str, help='Datahandlers to use',
    default=(None,), nargs='+', required=False,
    choices=list(DATAHANDLERS.keys()))
parser.add_argument(
    '--settings', type=str, nargs='+', action=StoreDict,
    help='Settings (e.g. overwrite:True)'
)

args, _ = parser.parse_known_args()


filename = args.filename

# Load json data
with open(filename) as json_file:
    data = json.load(json_file)

# Get list of problem_dicts
problem_dict_list = data['data']
num_problems = data['total']

# Construct list of Problem objects
problem_list = []
for problem_dict in problem_dict_list:
    problem_list.append(Problem(**problem_dict))

# Load settings, or set to empty dict
settings = args.settings if args.settings is not None else {}

# Create folder if needed
save_dir = args.save_dir
if save_dir and not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Extract general settings (not given by dicts)
general_kwargs = {}
for k, v in settings.items():
    if type(v) is not dict:
        general_kwargs[k] = v

# Construct some data
list_of_grades = []
for problem in problem_dict_list:
    grade = problem['grade']
    if grade not in list_of_grades:
        list_of_grades.append(grade)
list_of_grades.sort()

# Place initial data here, to allow datahandlers to change data
accumulated_data = {
    'problem_dict_list': problem_dict_list,
    'list_of_grades': list_of_grades,
    'problem_list': problem_list,
}

# Create and run datahandlers
for datahandler in args.datahandlers:
    # Skip if no datahandlers
    if datahandler is None:
        continue
    datahandler_class = DATAHANDLERS[datahandler]
    datahandler_obj = datahandler_class(save_dir)

    # Extract possible settings kwargs from args.settings
    kwargs = settings[datahandler] if datahandler in settings else {}
    # Run datahandler object, with different inputs, and settings dict
    returned_data = datahandler_obj(
        **{**accumulated_data, **general_kwargs, **kwargs},
    )
    if returned_data:
        accumulated_data = {**accumulated_data, **returned_data}
