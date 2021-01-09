from os import path
from bisect import insort
from collections import UserList

from common.exceptions import ParsingFailed
from .p_types import Script, Property, Event, Function
from .p_doc import Doc_Factory

class NamedList(UserList):
    def __init__(self, name):
        super().__init__([])
        self.name = name

    def to_md(self):
        return f"\n## {self.name}"

    def to_md_index(self):
        return f"\n### {self.name}"

class PapyDoc:
    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            file_doc, data = cls._parse_docs(file)
            return cls(file_doc, data)
    
    @staticmethod
    def _parse_docs(file):        
        file_doc = Doc_Factory(file)
        
        if not file_doc:
            raise ParsingFailed(EOFError("File is empty"))
        
        # We first make a dictionary
        # to easily map read Docs
        data = {
            Property : NamedList("Properties"),
            Event : NamedList("Events"),
            Function : NamedList("Functions")
        }
        
        if not isinstance(file_doc, Script):
            insort(data[type(file_doc)], file_doc)

            file_name = path.splitext(path.basename(file.name))[0].lower()
            file_doc = Script(file_name)

        while doc := Doc_Factory(file):
            insort(data[type(doc)], doc)

        # Convert data dict to a list,
        # with only non-empty NamedLists
        data = list((docs for docs in data.values() if docs))
        
        return file_doc, data

    def __init__(self, file_doc, data):
        self.file_doc = file_doc
        self.data = data

    def create_md_at(self, file_path):
        if not self.data:
            return
        
        file_name = self.file_doc.name + '.md'
        file_path = path.join(file_path, file_name)

        with open(file_path, 'w') as file:
            file.write(self.file_doc.to_md())
            file.write("\n\n## Overview")

            # Index
            for docs in self.data:
                file.write(docs.to_md_index())

                for doc in docs:
                    file.write(doc.to_md_index())

                file.write('\n')

            # Content
            for docs in self.data:
                file.write(docs.to_md())

                for doc in docs:
                    file.write(doc.to_md())

                file.write('\n')