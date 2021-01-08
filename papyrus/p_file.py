from os import path
from collections import UserList
from bisect import insort

from common.exceptions import ParsingFailed
from common.util import sanitize_line
from .p_types import Script, Property, Event, Function
from .p_doc import Doc_Factory

class Doc_Container(UserList):
    def __init__(self, name, type_):
        super().__init__([])
        self.name = name
        self.type_ = type_

    def insort(self, doc):
        if isinstance(doc, self.type_):
            return insort(self, doc)
        return False

    def to_md(self):
        return "\n## " + self.name

    def to_md_index(self):
        return "\n### " + self.name

class PapyDoc:
    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            file_doc, doc_containers = cls._parse_docs(file)
            return cls(file_doc, doc_containers)
    
    @staticmethod
    def _parse_docs(file):
        header = file.readline()

        if not header:
            raise ParsingFailed(EOFError())
        
        file.seek(0, 0)
        file_doc = Doc_Factory(file)
        
        if not file_doc:
            raise Exception("Has no documentation.")
        
        doc_containers = [
            Doc_Container("Properties", Property),
            Doc_Container("Events", Event),
            Doc_Container("Functions", Function)
        ]

        if not isinstance(file_doc, Script):
            for container in doc_containers:
                if container.append(file_doc):
                    break

            file_name = path.splitext(path.basename(file.name))[0].lower()
            file_doc = Script(sanitize_line(header), file_name, "", None)

        while doc := Doc_Factory(file):
            for container in doc_containers:
                if container.insort(doc):
                    break

        return file_doc, doc_containers

    def __init__(self, doc, doc_containers):
        self.doc = doc
        self.doc_containers = doc_containers

    def isempty(self):
        return not any(self.doc_containers)

    def create_md_at(self, file_path):
        if self.isempty():
            return
        
        file_name = self.doc.name + '.md'
        file_path = path.join(file_path, file_name)

        with open(file_path, 'w') as file:
            file.write(self.doc.to_md())
            file.write("\n\n## Overview")

            # Index
            for container in self.doc_containers:
                if container:
                    file.write(container.to_md_index())

                    for doc in container:
                        file.write(doc.to_md_index())

                    file.write("\n")

            # Content
            for container in self.doc_containers:
                if container:
                    file.write(container.to_md())

                    for doc in container:
                        file.write(doc.to_md())

                    file.write("\n")