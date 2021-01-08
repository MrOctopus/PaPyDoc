class ParsingFailed(Exception):
    def __init__(self, error):
        super().__init__("Parsing failed")
        self.error = error

class MalformedHeader(Exception):
    def __init__(self):
        super().__init__("Malformed Header")

class MalformedComment(Exception):
    def __init__(self):
        super().__init__("Malformed Comment")

class MalformedVariable(Exception):
    def __init__(self):
        super().__init__("Malformed variable")

class InvalidDataType(Exception):
    def __init__(self):
        super().__init__("Invalid data type")