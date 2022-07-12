from abc import ABC

#
# Abstract
#

class Var(ABC):
    NAME = ''

    def __init__(self, desc):
        self.desc = desc

    def to_md(self):
        return f"\n\n**{type(self).NAME.capitalize()}:**\n{self.desc}"

class Flag(Var):
    def to_md(self):
        type_name = type(self).NAME
        return f"\n\n* *Marked as **{type_name}***"

class Doc(ABC):
    NAME = ''
    IS_COMPLEX = False
    VALID_VARS = ()

    def __init__(self, name, header = "", desc = "", vars_ = None):
        self.name = name
        self.header = header
        self.desc = desc
        self.flags = []
        self.vars = []

        for var in vars_:
            (self.vars, self.flags)[isinstance(var, Flag)].append(var)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def to_md(self):
        return f"\n#### <a id=\"{self.name}\"></a> `{self.header}`\n{self.desc}{self.to_md_flags()}{self.to_md_vars()}\n***"

    def to_md_flags(self):
        if not self.flags:
            return ''

        return f"\n\n**Flags**:{''.join([flag.to_md() for flag in self.flags])}"

    def to_md_vars(self):
        if not self.vars:
            return ''

        return f"\n{''.join([var.to_md() for var in self.vars])}"

    def to_md_index(self):
        return f"\n* [{self.name}](#{self.name})"

#
# Variables
#

class Author(Var):
    NAME = 'author'

    def to_md(self):
        return f"\n### {type(self).NAME.capitalize()}: {self.desc}"

class Version(Var):
    NAME = 'version'

    def to_md(self):
        return f"\n### {type(self).NAME.capitalize()}: {self.desc}"

class Param(Var):
    NAME = 'param'

    def to_md(self):
        return f"\n* {self.desc}"

class Get(Var):
    NAME = 'get'

class Set(Var):
    NAME = 'set'

class Usage(Var):
    NAME = 'usage'

class Return(Var):
    NAME = 'return'

class Deprecated(Flag):
    NAME = 'deprecated'

class Override(Flag):
    NAME = 'override'

#
# Docs
#

class Doc_Param(Doc):
    def to_md_vars(self):
        if not self.vars:
            return ''

        params, rest = [], []

        for var in self.vars:
            (rest, params)[isinstance(var, Param)].append(var)

        var_str = ""

        if len(params) > 0:
            var_str = "\n\n**{}s:**{}".format(Param.NAME.capitalize(), ''.join([var.to_md() for var in params]))

        return var_str +  ''.join([var.to_md() for var in rest])

class Script(Doc):
    NAME = 'scriptname'
    IS_COMPLEX = True
    VALID_VARS = (
        Author,
        Version
    )

    def to_md(self):
        return f"# Documentation ({self.name}){self.to_md_vars()}\n{self.desc}"

class Property(Doc):
    NAME = 'property'
    IS_COMPLEX = True
    VALID_VARS = (
        Get,
        Set,
        Usage,
        Deprecated
    )

class Event(Doc_Param):
    NAME = 'event'
    VALID_VARS = (
        Param,
        Usage,
        Deprecated,
        Override
    )

class Function(Doc_Param):
    NAME = 'function'
    VALID_VARS = (
        Param,
        Usage,
        Return,
        Deprecated,
        Override
    )


#
# Types
#

VAR_TYPES = (
    Author,
    Version,
    Param,
    Get,
    Set,
    Usage,
    Return,
    Deprecated,
    Override
)

DOC_TYPES = (
    Script,
    Property,
    Event,
    Function
)