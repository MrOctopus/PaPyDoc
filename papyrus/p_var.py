from common.defines import DOC_VAR
from common.exceptions import MalformedVariable, InvalidDataType
from .p_types import VAR_TYPES

class Var_Factory:
    def __new__(cls, comment):
        type_, description = cls._parse_var(comment)
        return type_(description)

    @staticmethod
    def _parse_var(comment):
        type_string, unused, description = comment.popleft().partition(' ')

        # String could not be partitioned
        # so type cannot be determined
        if len(description) < 1:
            raise MalformedVariable()

        type_string = type_string.lower()
        matches = (x for x in VAR_TYPES if type_string == x.NAME)

        try:
            type_ = next(matches)
            description += '\n'

            while comment:
                line = comment.popleft()

                if line[0] is DOC_VAR:
                    comment.appendleft(line[1:])
                    break

                description += line + '\n'

            return type_, description[:-1]
        except StopIteration:
            raise InvalidDataType()