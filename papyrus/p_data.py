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
    TYPES = {
        Script.NAME : Script,
        Property.NAME : Property,
        Event.NAME : Event,
        Function.NAME : Function
    }

    def __new__(cls, header, comment):
        #data_type = cls._get_type(header)
        
        desc = cls._parse(comment)
        desc_len = len(desc)

        if desc_len < len(comment):
            variables = cls._parse_vars(comment[desc_len + 1:])

        return Data(desc, vars_)

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
    def _parse(comment):    
        i = 0

        for line in comment:
            if line[0] is DOC_VAR:
                break
            i += 1

        return comment[0:i]

    @staticmethod
    def _parse_vars(type, variables):
        vars_ = []
        
        while (var := Var_Factory(file)):
            if not var.__class__ in type.VALID_VARS:
                raise Exception()

            if not var.__class__ == Param and any(x.__class__ is var.__class__ for x in vars_):
                raise Exception()

            vars_.append(var)

        return vars_