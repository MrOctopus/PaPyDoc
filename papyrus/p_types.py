from abc import ABC

#
# Abstract
#

class Var(ABC):
    NAME = ''

    def __init__(self, desc):
        self.desc = desc

    def to_md(self):
        return "\n\n##### {}:\n{}".format(self.__class__.NAME.capitalize(), self.desc)

class Doc(ABC):
    NAME = ''
    IS_COMPLEX = False
    VALID_VARS = ()

    def __init__(self, header, name, desc, vars_):
        self.header = header
        self.name = name
        self.desc = desc
        self.vars_ = vars_

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def to_md(self):
        return "\n#### <a id=\"{}\"></a> `{}`\n{}{}\n***".format(self.name, self.header, self.desc, self.to_md_vars())

    def to_md_vars(self):
        if not self.vars_:
            return ''

        return '\n' + ''.join([var.to_md() for var in self.vars_])

    def to_md_index(self):
        return "\n* [{0}](#{0})".format(self.name)

#
# Variables
#

class Author(Var):
    NAME = 'author'

    def to_md(self):
        return "\n### {}: {}".format(self.__class__.NAME.capitalize(), self.desc)

class Version(Var):
    NAME = 'version'

    def to_md(self):
        return "\n### {}: {}".format(self.__class__.NAME.capitalize(), self.desc)

class Param(Var):
    NAME = 'param'

    def to_md(self):
        return "\n* " + self.desc

class Get(Var):
    NAME = 'get'

class Set(Var):
    NAME = 'set'

class Usage(Var):
    NAME = 'usage'

class Return(Var):
    NAME = 'return'

#
# Docs
#

class Doc_Param(Doc):
    def to_md_vars(self):
        if not self.vars_:
            return ''

        params, rest = [], []

        for var in self.vars_:
            (rest, params)[isinstance(var, Param)].append(var)

        var_str = ""

        if len(params) > 0:
            var_str = "\n\n##### {}s:{}".format(Param.NAME.capitalize(), ''.join([var.to_md() for var in params]))

        return var_str +  ''.join([var.to_md() for var in rest])

class Script(Doc):
    NAME = 'scriptname'
    IS_COMPLEX = True
    VALID_VARS = (
        Author,
        Version
    )

    def to_md(self):
        return "# Documentation ({}){}\n{}".format(self.name, self.to_md_vars(), self.desc)

class Property(Doc):
    NAME = 'property'
    IS_COMPLEX = True
    VALID_VARS = (
        Get,
        Set,
        Usage
    )

class Event(Doc_Param):
    NAME = 'event'
    VALID_VARS = (
        Param,
        Usage
    )

class Function(Doc_Param):
    NAME = 'function'
    VALID_VARS = (
        Param,
        Usage,
        Return
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
    Return
)

DOC_TYPES = (
    Script,
    Property,
    Event,
    Function
)