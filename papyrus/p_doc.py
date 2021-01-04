from collections import UserList
from bisect import insort
from functools import partial

from common.defines import DOC_START, DOC_END
from common.util import sanitize_line, read_until

from .p_data import Script, Property, Event, Function

class Doc:
    def __init__(self, header, data):
        self.header = header
        self.data = data

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def _get_name(self, header, type_):
        start_index = header_lower.find(type_)
            
        if start_index == -1:
            raise Exception()

        start_index = start_index + len(type_) + 1

        if type_ in (Script.NAME, Property.NAME):
            end_index = header_lower.find(' ', start_index)

            if end_index != -1:
                return header[start_index:end_index]
            else:
                return header[start_index:]
        
        elif (end_index := header_lower.find('(', start_index)) != -1:
            return header[start_index:end_index]

        raise Exception()

    def to_md(self):
        return "\n#### <a id=\"{}\"></a> `{}`{}\n***".format(self.name, self.header, self.data.to_md())

    def to_md_index(self):
        return "\n* [{0}](#{0})".format(self.name)

class Doc_Container(UserList):
    def __init__(self, name, type_):
        super().__init__([])
        self.name = name
        self.type_ = type_

    def insort(self, doc):
        if isinstance(doc.data, self.type_):
            return insort(self, doc)
        return False

    def to_md(self):
        return "\n## " + self.name

    def to_md_index(self):
        return "\n### " + self.name

class Doc_Factory:
    def __new__(cls, file):
        try:
            header, comment = cls._next_doc(file)

            data = Data_Factory(header, comment)

            if isinstance(data, Property) and not header_lower.endswith(('auto', 'autoreadonly')):
                read_until(file, cls.property_ends)

            return Doc(header, data)
        except EOFError:
            return None

    @classmethod
    def _next_doc(cls, file):
        header, line = read_until(file, cls.comment_starts)
        comment = []

        if len(line) == 1 or not cls.comment_ends(line[1:], comment = comment):
            try:
                comment_ends_partial = partial(cls.comment_ends, comment = comment)
                read_until(file, comment_ends_partial)
            except EOFError:
                raise Exception("Malformed comment")

        return sanitize_line(header), comment

    @staticmethod
    def comment_starts(line):
        if line[0] is DOC_START:
            return True
        
        return False

    @staticmethod
    def comment_ends(line, comment):
        index = line.find(DOC_END)
        
        if index != -1:
            if index > 0:
                comment.append(line[:index])
            return True

        comment.append(line)
        return False

    @staticmethod
    def property_ends(line):
        if line.lower().startswith("endproperty"):
            return True
        
        return False
