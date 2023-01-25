import json
import argparse
import os

from datahandlers.data import DATAHANDLERS
from utils.utils import StoreDict, Problem, LogbookEntry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help='Path to dataset files', nargs='*',
                        default='MoonBoard/problems MoonBoard 2016 .json')
    parser.add_argument('--logbook', help='Path to logbook file',
                        default='MoonBoard/logbook.json')
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
        problem_data = json.load(json_file)

    # Load logbook
    with open(args.logbook) as json_file:
        logbook_data = json.load(json_file)

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

    # Construct input data in 'accumulated_data' dict
    # Place initial data here, to allow datahandlers to change data
    accumulated_data = construct_data(problem_data, logbook_data)

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


def get_benchmark_problems(
        cache_folder='benchmark_problems',
        day_limit=5,
):
    holdset_name_list = [
        'MoonBoard 2016 ',
        'MoonBoard Masters 2017 25',
        'MoonBoard Masters 2017 40',
        'MoonBoard Masters 2019 25',
        'MoonBoard Masters 2019 40',
        'Mini MoonBoard 2020 40',
        ]

    # Make sure cache folder exists
    import os
    if not os.path.isdir(cache_folder):
        os.makedirs(cache_folder)

    # Dict to hold lists of problems
    benchmark_problems_dict = {}
    benchmark_grades_dict = {}

    # Loop all holdsets
    for holdset in holdset_name_list:
        filename = f'problems {holdset}.json'

        # Load BM data from cache, or construct
        cache_file = os.path.join(cache_folder, filename)
        if os.path.exists(cache_file):
            # Cache exists -> Load benchmark data
            with open(cache_file) as json_file:
                benchmark_data = json.load(json_file)
        else:
            # Don't exist -> Construct benchmark data
            problem_file = os.path.join('MoonBoard', filename)
            benchmark_data = []
            with open(problem_file) as json_file:
                problem_data = json.load(json_file)
            for problem in problem_data['data']:
                if problem['isBenchmark']:
                    benchmark_data.append(problem)
            json_object = json.dumps(benchmark_data, indent=4)
            with open(cache_file, "w") as outfile:
                outfile.write(json_object)

        # Go through BM data and create list of Problem objects
        problem_list = []
        for problem_dict in benchmark_data:
            problem_list.append(Problem(**problem_dict))
        benchmark_problems_dict[holdset] = problem_list

        # Create 'list' of all bm grades for this holdset
        # (or actually a mapping from grades to int
        grade_list = []
        for bm in problem_list:
            if bm.grade not in grade_list:
                grade_list.append(bm.grade)
        grade_list.sort()
        # Make a mapping from str grade to int
        grade_int_mapping = {}
        for i, grade in enumerate(grade_list):
            grade_int_mapping[grade] = i
        # Assign to a dict with holdset as key
        benchmark_grades_dict[holdset] = grade_int_mapping

    return (benchmark_problems_dict, benchmark_grades_dict)


def construct_data(problem_data, logbook_data):
    '''
    Construct useful data from loaded problems and logbook

    Args:
      problem_data: loaded from json
      logbook_data: loaded from json
    '''
    # Get benchmark problems and grades
    (benchmark_problems_dict, benchmark_grades_dict) = get_benchmark_problems()

    # Get list of problem_dicts
    problem_dict_list = problem_data['data']

    # Construct list of Problem objects
    problem_list = []
    for problem_dict in problem_dict_list:
        problem_list.append(Problem(**problem_dict))

    # Construct list of LogbookEntry objects
    logbook_dict = {}
    for log in logbook_data:
        logbook_entry = LogbookEntry(**log)
        logbook_dict[logbook_entry.apiId] = logbook_entry

    # Construct 'list_of_grades'
    list_of_grades = []
    for problem in problem_dict_list:
        grade = problem['grade']
        if grade not in list_of_grades:
            list_of_grades.append(grade)
    list_of_grades.sort()

    # Construct benchmark list
    benchmark_list = [p for p in problem_list if p.isBenchmark]
    list_of_bm_grades = []

    # Construct 'list_of_bm_grades'
    for bm in benchmark_list:
        if bm.grade not in list_of_bm_grades:
            list_of_bm_grades.append(bm.grade)
    list_of_bm_grades.sort()

    # Return dict of different lists
    data = {
        'problem_dict_list': problem_dict_list,
        'list_of_grades': list_of_grades,
        'list_of_bm_grades': list_of_bm_grades,
        'problem_list': problem_list,
        'benchmark_list': benchmark_list,
        'logbook_data': logbook_data,
        'logbook_dict': logbook_dict,
        'benchmark_problems_dict': benchmark_problems_dict,
        'benchmark_grades_dict': benchmark_grades_dict,
    }

    return data


if __name__ == '__main__':
    main()
