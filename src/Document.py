from __future__ import annotations
from Stemer import Stemer
from Index import Index
import os
import re


class Document:

    def __init__(self, dictInfoDocument: dict[str, str]):
        self.id = dictInfoDocument.get("DOCNO").strip()
        self.dictInfoDocument = dictInfoDocument

    def readFile(file) -> list[Document]:
        listDocuments: list[Document] = []
        document: dict[str, str]
        readInfo: str = ""
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "<DOC>" in line:
                    document = {
                        "DOCNO": "",
                        "FILEID": "",
                        "NOTE": "",
                        "UNK": "",
                        "FIRST": "",
                        "SECOND": "",
                        "HEAD": "",
                        "DATELINE": "",
                        "TEXT": "",
                        "BYLINE": "",
                    }
                for key in document.keys():
                    if "<" + key + ">" in line:
                        line = line.replace("<" + key + ">", "")
                        readInfo = key
                    if "</" + key + ">" in line:
                        line = line.replace("</" + key + ">", "")
                        document[key] += line
                        readInfo = ""
                if readInfo != "":
                    document[readInfo] += line
                if "</DOC>" in line:
                    listDocuments.append(Document(document))
        return listDocuments

    def loadDocuments(directory) -> list[Document]:
        listDocuments: list[Document] = []
        files: list[str] = os.listdir(directory)
        for file in files:
            if file.endswith(".txt"):
                listDocuments.extend(Document.readFile(directory + "/" + file))
        return listDocuments

    def indexing(self, stemer: Stemer, index: Index):
        text: str = self.dictInfoDocument.get("TEXT").lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        listWord = text.split()
        i: int = 0
        for word in listWord:
            i += 1
            index.Add(stemer.stemerize(word), self.id, i)
