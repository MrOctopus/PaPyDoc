from collections import UserList
from bisect import insort
from functools import partial

from common.defines import DOC_START, DOC_END
from common.exceptions import ParsingFailed, MalformedHeader, MalformedComment
from common.util import sanitize_line, read_until

from .p_data import Script, Property, Event, Function, Data_Factory

class Doc:
    def __init__(self, header, name, data):
        self.header = header
        self.name = name
        self.data = data

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

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
            header, comment = cls._get_next_doc(file)
            data = Data_Factory(header, comment)
            
            #if isinstance(data, Property) and not header_lower.endswith(('auto', 'autoreadonly')):
            #    read_until(file, cls.property_ends)

            return Doc(header, data)
        except EOFError:
            return None
        except Exception as e:
            raise ParsingFailed(e)

    @classmethod
    def _get_next_doc(cls, file):
        header, line = read_until(file, cls.comment_starts)
        comment = []

        # This looks complicated, so here's an explanation:
        # If len(line) is == 1, that means the only char is the start block on the line,
        # and therefore we wish to read_until we find the end block.
        # If len(line) is not 1 (-> or), that implies there are several chars on the line.
        # We therefore attempt to find the end block on the same line, appending
        # the chars from after the start block [1:] to the comment. If there is no end block,
        # we read_until we find the end block.
        if len(line) == 1 or not cls.comment_ends(line[1:], read_lines = comment):
            try:
                read_until(file, partial(cls.comment_ends, read_lines = comment))
            except EOFError:
                raise MalformedComment()

        return sanitize_line(header), comment

    @classmethod
    def _parse_name(cls):
        header_lower = self.header.lower()

        start_index = header_lower.find(self.data.NAME)

        if start_index == -1:
            raise MalformedHeader()

        start_index = start_index + len(self.data.NAME) + 1

        if self.data.NAME in (Script.NAME, Property.NAME):
            end_index = header_lower.find(' ', start_index)

            if end_index != -1:
                return self.header[start_index:end_index]
            else:
                return self.header[start_index:]
        
        elif (end_index := header_lower.find('(', start_index)) != -1:
            return self.header[start_index:end_index]

        raise MalformedHeader()

    @staticmethod
    def comment_starts(line):
        if line[0] is DOC_START:
            return True
        
        return False

    @staticmethod
    def comment_ends(line, read_lines):
        index = line.find(DOC_END)
        
        if index != -1:
            if index > 0:
                read_lines.append(line[:index])
            return True

        read_lines.append(line)
        return False

    @staticmethod
    def property_ends(line):
        if line.lower().startswith("endproperty"):
            return True
        
        return False
