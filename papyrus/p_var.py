from abc import ABC
from common.defines import DOC_VAR, DOC_END

class Var_Factory:
    def __new__(cls, type_, comment):
        type_, desc = cls._parse_var(file)

        if not var.__class__ in type.VALID_VARS:
                raise Exception()

        if not type_:
            return None

        return VAR_TYPES[type_](desc)

    @staticmethod
    def _parse_var(file):
        line = file.readline().strip()
        
        if line[0] == DOC_END:
            return None, None
        
        line = line.split(' ')

        if len(line) <= 1:
            raise Exception()

        type_ = line[0]

        if len(type_) <= 1:
            raise Exception()

        type_ = type_[1:].lower()
        desc = ' '.join(line[1:]) + '\n'

        while True:
            prev_pos = file.tell()
            line = file.readline()
            
            if not line:
                raise Exception()
            
            line = line.strip()

            if not line:
                continue

            if line[0] == DOC_VAR or line[0] == DOC_END:
                file.seek(prev_pos)
                break
            
            desc = desc + line + '\n'

        return type_, desc[:-1]