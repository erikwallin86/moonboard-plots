import argparse


class Move():
    def __init__(self, **kwargs):
        # Assign kwargs directly to __dict__
        self.__dict__ = kwargs

    def __repr__(self):
        # Some compact formatting
        message = f'{self.description}'
        if self.isStart:
            message += "=start"
        if self.isEnd:
            message += "=end"
        return f"'{message}'"


class Problem():
    def __init__(self, moves=None, **kwargs):
        # Assign kwargs directly to __dict__
        self.__dict__ = kwargs

        # list[move_dict] -> list[Move]
        self.moves = []
        for move_dict in moves:
            self.moves.append(Move(**move_dict))

    def __repr__(self):
        message = f"name='{self.name}',grade='{self.grade}',moves={self.moves}"

        return f'{self.__class__.__name__}({message})'


class LogbookEntry():
    def __init__(self, problem, **kwargs):
        # Assign kwargs directly to __dict__
        self.__dict__ = kwargs

        # Retrieve apiId from 'problem'
        self.apiId = problem['apiId']

    def __repr__(self):
        message = f"apiId='{self.apiId}',grade='{self.grade}',entryDate={self.entryDate}"

        return f'{self.__class__.__name__}({message})'


class StoreDict(argparse.Action):
    """
    Custom argparse action for storing dict.

    In: args1:0.0 args2:"dict(a=1)"
    Out: {'args1': 0.0, arg2: dict(a=1)}
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreDict, self).__init__(option_strings,
                                        dest,
                                        nargs=nargs,
                                        **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        arg_dict = {}
        for arguments in values:
            arg_dict_local = self.split(arguments)
            arg_dict = {**arg_dict, **arg_dict_local}
        setattr(namespace, self.dest, arg_dict)

    def split(self, arguments):
        arg_dict = {}
        key = arguments.split(":")[0]
        value = ":".join(arguments.split(":")[1:])
        # Evaluate the string as python code
        try:
            if ':' in value:
                arg_dict_lower = self.split(value)
                arg_dict[key] = arg_dict_lower
            else:
                arg_dict[key] = eval(value)
        except NameError:
            arg_dict[key] = value
        except SyntaxError:
            return {key: value}

        return arg_dict


def add_dicts(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]

    return dict1
