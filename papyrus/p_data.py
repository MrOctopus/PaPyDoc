from abc import ABC
from common.defines import DOC_VAR
from .p_var import Var, Author, Version, Get, Set, Usage, Param, Return

class Data(ABC):
    NAME = ''
    VALID_VARS = ()

    def __init__(self, desc = "", vars_ = None):
        self.desc = desc
        self.vars_ = vars_

    def to_md(self):
        return "\n{}{}".format(self.desc, self.to_md_vars())

    def to_md_vars(self):
        if not self.vars_:
            return ''

        return '\n' + ''.join([var.to_md() for var in self.vars_])

class Data_Param(Data):
    def to_md_vars(self):
        if not self.vars_:
            return ''

        params, rest = [], []

        for var in self.vars_:
            (rest, params)[var.__class__ is Param].append(var)

        var_str = ""

        if len(params) > 0:
            var_str = "\n\n##### {}s:{}".format(Param.NAME.capitalize(), ''.join([var.to_md() for var in params]))

        return var_str +  ''.join([var.to_md() for var in rest])

class Script(Data):
    NAME = 'scriptname'
    VALID_VARS = (
        Author,
        Version
    )

    def to_md(self):
        return "{}\n{}".format(self.to_md_vars(), self.desc)

class Property(Data):
    NAME = 'property'
    VALID_VARS = (
        Get,
        Set,
        Usage
    )

class Event(Data_Param):
    NAME = 'event'
    VALID_VARS = (
        Param,
        Usage
    )


class Function(Data_Param):
    NAME = 'function'
    VALID_VARS = (
        Param,
        Usage,
        Return
    )

class Data_Factory:
    def __new__(cls, header, comment):
        data_type = cls._get_type(header)
        
        desc = cls._parse_desc(comment)
        
        if variables:
            cls._parse_vars(variables)

        return cls(desc, vars_)

    @staticmethod
    def _get_type(header):
        header = header.lower()

        for key in DATA_TYPES:
            type_index = header_lower.find(key)
            if type_index != -1:
                return key

        # Could not find type
        raise Exception("No valid type!")

    @staticmethod
    def _parse_desc(file):
        has_vars = False
        desc = ""

        
            
            desc += line + '\n'

        return has_vars, desc[:-1]

    @staticmethod
    def _parse_vars(cls, file):
        vars_ = []
        
        while (var := Var_Factory(file)):
            if not var.__class__ in cls.VALID_VARS:
                raise Exception()

            if not var.__class__ == Param and any(x.__class__ is var.__class__ for x in vars_):
                raise Exception()

            vars_.append(var)

        return vars_