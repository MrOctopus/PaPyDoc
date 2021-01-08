from collections import deque
from functools import partial

from common.defines import DOC_START, DOC_END, DOC_VAR
from common.exceptions import ParsingFailed, MalformedHeader, MalformedComment, InvalidDataType
from common.util import sanitize_line, read_until

from .p_types import VAR_TYPES, DOC_TYPES, Property, Doc_Param, Param
from .p_var import Var_Factory

class Doc_Factory:
    def __new__(cls, file):
        try:
            # Header and comment
            header, comment = cls._get_next_doc(file)
            header_lower = header.lower()
            
            # Parse
            type_ = cls._parse_type(header_lower)
            name = cls._parse_name(header, header_lower, type_)
            description = cls._parse_description(comment)
            #variables = cls._parse_variables(type_, comment)
            variables = None

            print(description)

            # Skip if property contains functions
            if type_ is Property and not header_lower.endswith(('auto', 'autoreadonly')):
                read_until(file, cls.property_ends)

            return type_(header, name, description, variables)
        except EOFError:
            return None
        except Exception as e:
            raise ParsingFailed(e)

    @classmethod
    def _get_next_doc(cls, file):
        header, line = read_until(file, cls.comment_starts)
        comment = deque([])

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

    @staticmethod
    def _parse_type(header_lower):
        matches = (type_ for type_ in DOC_TYPES if header_lower.find(type_.NAME) != -1)

        try:
            return next(matches)
        except StopIteration:
            raise InvalidDataType()

    @staticmethod
    def _parse_name(header, header_lower, type_):
        start_index = header_lower.find(type_.NAME)

        if start_index == -1:
            raise MalformedHeader()

        start_index = start_index + len(type_.NAME) + 1

        if type_.IS_COMPLEX:
            end_index = header_lower.find(' ', start_index)

            if end_index != -1:
                return header[start_index:end_index]
            else:
                return header[start_index:]
        
        elif (end_index := header_lower.find('(', start_index)) != -1:
            return header[start_index:end_index]

        raise MalformedHeader()

    @staticmethod
    def _parse_description(comment):    
        description = ""

        while comment:
            line = comment.popleft()

            if not line[0] is DOC_VAR:
                description += line + '\n'
            elif len(line) > 1:
                comment.appendleft(line[1:])

            break

        return description[:-1]

    @staticmethod
    def _parse_variables(data_type, comment):
        variables = []

        while (var := Var_Factory(data_type, comment)):
            variables.append(var)        

        if not isinstance(data_type, Doc_Param) and sum(isinstance(var, Param) for var in variables) > 1:
            raise Exception()

        return variables

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
