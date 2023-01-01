import sys
import inspect
import os
import numpy as np
from datetime import datetime
import matplotlib
import colorcet as cc


class DataHandler():
    '''
    Base class for datahandler
    '''
    def __init__(self, save_dir):
        self.save_dir = save_dir

    def __call__(self, logger=None, **kwargs):
        # Return kwargs which are not 'input'/'data'
        return kwargs


class PrintInfo(DataHandler):
    '''
    Print info about dataset
    '''
    def __call__(self, problem_list=None,
                 overwrite=False,
                 **kwargs):
        print(f"Number of problems: {len(problem_list)}")
        benchmarks = [p for p in problem_list if p.isBenchmark]
        print(f"Number of benchmarks:{len(benchmarks)}")

        # Make list of grades
        list_of_grades = []
        for bm in benchmarks:
            grade = bm.grade
            if grade not in list_of_grades:
                list_of_grades.append(grade)
        list_of_grades.sort()

        # Prepare dict of benchmark list, per grade
        benchmark_per_grade = {}
        # Initialize empty list
        for grade in list_of_grades:
            benchmark_per_grade[grade] = []

        # Loop benchmarks and add to sublists
        for bm in benchmarks:
            grade = bm.grade
            benchmark_per_grade[grade].append(bm)

        print("Benchmarks per grade")
        for grade, bm_list in benchmark_per_grade.items():
            print(f"  {grade}: {len(bm_list)}")


class Benchmarks(DataHandler):
    '''
    Produce Problem view for all benchmark problems
    '''
    def __call__(self, problem_list=None,
                 overwrite=False,
                 **kwargs):
        # Update save_dir with 'class name' subfolder:
        class_name = self.__class__.__name__
        self.save_dir = os.path.join(self.save_dir, class_name)
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        # Get list of all benchmark problems
        benchmarks = [p for p in problem_list if p.isBenchmark]

        # Loop benchmarks and plot problems
        for bm in benchmarks:
            # Validate name.
            # Can not containt slash
            # This would be good to do with descriptor?
            name = bm.name.replace('/', '_')
            grade = bm.grade
            filename = f"{name}_{grade}.png"
            filename = os.path.join(self.save_dir, filename)
            print(f"filename:{filename}")
            if os.path.exists(filename) and not overwrite:
                # Skip if file already exists
                continue

            list_of_moves = bm.moves
            from plots.plot import plot_problem
            fig, ax = plot_problem(list_of_moves)
            fig.savefig(filename)


class BenchmarkHoldFrequency(DataHandler):
    '''
    For each grade, visualize which holds are used the most
    '''
    def __call__(self,
                 problem_list,
                 list_of_grades,
                 overwrite=False,
                 **kwargs):
        # Update save_dir with 'class name' subfolder:
        class_name = self.__class__.__name__
        self.save_dir = os.path.join(self.save_dir, class_name)
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        # Get list of all benchmark problems
        benchmarks = [p for p in problem_list if p.isBenchmark]

        from utils.utils import add_dicts
        for grade in list_of_grades:
            print(f"grade:{grade}")
            filename = f"frequency_{grade}.png"
            filename = os.path.join(self.save_dir, filename)
            if os.path.exists(filename) and not overwrite:
                # Skip if file already exists
                continue

            holds_sum_dict = {}
            # Loop benchmarks and plot problems
            for bm in benchmarks:
                if bm.grade != grade:
                    continue

                # Accumulate moves
                list_of_moves = bm.moves
                moves_dict = {}
                for move in list_of_moves:
                    moves_dict[move.description] = 1
                holds_sum_dict = add_dicts(holds_sum_dict, moves_dict)

            from plots.plot import plot_frequency
            if len(holds_sum_dict) > 0:
                fig, ax = plot_frequency(holds_sum_dict)
                fig.savefig(filename)


class HoldFrequency(DataHandler):
    '''
    For each grade, visualize which holds are used the most
    '''
    def __call__(self,
                 problem_list,
                 list_of_grades,
                 overwrite=False,
                 **kwargs):
        # Update save_dir with 'class name' subfolder:
        class_name = self.__class__.__name__
        self.save_dir = os.path.join(self.save_dir, class_name)
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        from utils.utils import add_dicts
        for grade in list_of_grades:
            print(f"grade:{grade}")
            filename = f"frequency_{grade}.png"
            filename = os.path.join(self.save_dir, filename)
            if os.path.exists(filename) and not overwrite:
                # Skip if file already exists
                continue

            holds_sum_dict = {}
            # Loop benchmarks and plot problems
            for problem in problem_list:
                if problem.grade != grade:
                    continue

                # Accumulate moves
                moves_dict = {}
                for move in problem.moves:
                    moves_dict[move.description] = 1
                holds_sum_dict = add_dicts(holds_sum_dict, moves_dict)

            from plots.plot import plot_frequency
            if len(holds_sum_dict) > 0:
                fig, ax = plot_frequency(holds_sum_dict)
                fig.savefig(filename)


class Logbook(DataHandler):
    '''
    Test with logbook
    '''
    def __call__(self,
                 problem_list,
                 list_of_bm_grades,
                 logbook_dict,
                 overwrite=False,
                 cmap=cc.cm.rainbow,
                 dpi=200,
                 **kwargs):
        # Update save_dir with 'class name' subfolder:
        class_name = self.__class__.__name__
        # self.save_dir = os.path.join(self.save_dir, class_name)
        # if not os.path.isdir(self.save_dir):
        #     os.makedirs(self.save_dir)

        filename = f"{class_name}.png"
        filename = os.path.join(self.save_dir, filename)
        if os.path.exists(filename) and not overwrite:
            # Skip if file already exists
            return False

        # Make a mapping from str grade to int
        grade_to_int = {}
        for i, grade in enumerate(list_of_bm_grades):
            grade_to_int[grade] = i

        # Make 'problem_dict' with id as key
        problem_dict = {}
        for problem in problem_list:
            problem_dict[problem.apiId] = problem

        # Extract 2016 problems from logbook
        # (indirectly, as problem_dict only contains 2016 problems for me)
        logbook_2016 = {
            k: v for k, v in logbook_dict.items() if k in problem_dict}
        # Sort logbook by entry-date
        logbook_2016 = dict(sorted(
            logbook_2016.items(),
            key=lambda item: item[1].entryDate))

        # Prepare lists
        dates = []
        num_problems = []
        grades = []
        # Loop all logbook_2016 entries
        for i, (api_id, entry) in enumerate(logbook_2016.items()):
            # Remove fractions of seconds from entry date
            cut_date = entry.entryDate.split('.')[0]
            date = datetime.strptime(cut_date, "%Y-%m-%dT%H:%M:%S")
            dates.append(date)
            num_problems.append(i+1)

            # Get problem grade
            problem = problem_dict[api_id]
            grades.append(grade_to_int[problem.grade])

        # Produce 'color-array' depending on the grade
        grades = np.divide(grades, len(list_of_bm_grades)-1)
        colors = cmap(grades)

        # Plot as scatter plot
        from plots.plot import new_fig
        fig, ax = new_fig()
        ax.set_axisbelow(True)
        ax.grid(which='minor', linewidth=0.5)
        ax.grid(which='major', linewidth=1.5)

        ax.scatter(dates, num_problems, color=colors, edgecolors='k',
                   linewidth=0.5)

        # Construct custom legend
        import matplotlib.lines as mlines
        handles = []
        for i, g in enumerate(list_of_bm_grades):
            color = cmap(i/(len(list_of_bm_grades)-1))
            marker = mlines.Line2D(
                [], [], marker='o', linestyle='None', label=g, color=color,
                markeredgewidth=0.5, markeredgecolor='k')
            handles.append(marker)
        ax.legend(handles=handles, loc='right', bbox_to_anchor=(1.2, 0.5))

        # Setup axis labels, tics etc.
        ax.set_xlabel('Date')
        ax.set_ylabel('Benchmark problems')

        ax.set_ylim(bottom=0)

        ax.xaxis.set_major_locator(matplotlib.dates.YearLocator())
        ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y'))
        ax.xaxis.set_minor_locator(matplotlib.dates.MonthLocator())

        fig.savefig(filename, dpi=dpi, bbox_inches="tight")


class RepeatsHistogram(DataHandler):
    '''
    Produce histogram showing how many repeats problems typically have
    '''
    def __call__(self,
                 problem_list,
                 list_of_grades,
                 overwrite=False,
                 **kwargs):
        # Update save_dir with 'class name' subfolder:
        class_name = self.__class__.__name__
        self.save_dir = os.path.join(self.save_dir, class_name)
        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        filename = "repeats.png"
        filename = os.path.join(self.save_dir, filename)
        if os.path.exists(filename) and not overwrite:
            return False

        list_of_repeats = []
        for problem in problem_list:
            list_of_repeats.append(problem.repeats)

        # # Log
        # bins = [0, 1, 10, 100, 1000, 10000, 100000]
        # hist, bin_edges = np.histogram(list_of_repeats, bins=bins)
        # from plots.plot import new_fig
        # fig, ax = new_fig()
        # width = np.multiply(bins[1:], 0.1)
        # bar = ax.bar(bin_edges[:-1], hist, width=width)
        # ax.bar_label(bar)
        # ax.set_xscale('log')
        # fig.savefig(filename)

        # Linear
        bins = range(0, 1000, 50)
        hist, bin_edges = np.histogram(list_of_repeats, bins=bins)
        from plots.plot import new_fig
        fig, ax = new_fig()
        bar = ax.bar(bin_edges[:-1], hist, width=(bins[1]-bins[0])*0.8)

        print(f"len(list_of_repeats):{len(list_of_repeats)}")

        ax.set_xlabel('Num repeats')
        ax.set_ylabel('Num problems?')

        ax.bar_label(bar)
        # ax.set_ylim([0, 1e+4])
        ax.set_yscale('log')
        fig.savefig(filename)


# Make a dict of all datahandlers, as dict[name, class]
clsmembers_pairs = inspect.getmembers(sys.modules[__name__], inspect.isclass)
DATAHANDLERS = {k: v for (k, v) in clsmembers_pairs if k != 'DataHandler'}