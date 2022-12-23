import sys
import inspect
import os
import numpy as np


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
