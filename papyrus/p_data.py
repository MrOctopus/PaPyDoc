from abc import ABC
from common.defines import DOC_VAR
from common.exceptions import InvalidDataType
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
    TYPES = (
        Script,
        Property,
        Event,
        Function
    )

    def __new__(cls, header, comment):
        data_type = cls._parse_type(header)
        description = cls._parse_description(comment)
        variables = None

        # If description length is < comment length,
        # we need to parse variable data
        if (desc_len := len(description)) < len(comment):
            variables = cls._parse_variables(data_type, comment[desc_len + 1:])

        return data_type('\n'.join(description), variables)

    @classmethod
    def _parse_type(cls, header):
        header = header.lower()
        matches = (type_ for type_ in cls.TYPES if header.find(type_.NAME))

        if data_type := next(matches):
            return data_type

        raise InvalidDataType()

    @staticmethod
    def _parse_description(comment):    
        i = 0

        for line in comment:
            if line[0] is DOC_VAR:
                break
            i += 1

        return comment[0:i]

    @staticmethod
    def _parse_variables(data_type, comment):
        vars_ = []
        start = 0
        end = 0

        for line in comment:
            if line[0] is DOC_VAR
        
        while (var := Var_Factory(data_type, comment)):
            vars_.append(var)        

        if not isinstance(data_type, Data_Param) and sum(isinstance(var, Param) for var in variables) > 1:
            raise Exception()

        return vars_