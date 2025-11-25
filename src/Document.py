from __future__ import annotations
from Stemer import Stemer
from StopWords import StopWords
from Index import Index
import os
import re


class Document:
    id: str
    dictInfoDocument: dict[str, str]
    stop_words: StopWords

    def __init__(self, dictInfoDocument: dict[str, str], stop_words: StopWords):
        self.id = dictInfoDocument.get("DOCNO").strip()
        self.dictInfoDocument = dictInfoDocument
        self.stop_words = stop_words

    def readFile(file, stop_words: StopWords) -> list[Document]:
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
                    listDocuments.append(Document(document, stop_words))
        return listDocuments

    def loadDocuments(directory, stop_words: StopWords) -> list[Document]:
        listDocuments: list[Document] = []
        files: list[str] = os.listdir(directory)
        for file in files:
            if file.endswith(".txt"):
                listDocuments.extend(Document.readFile(directory + "/" + file, stop_words))
        return listDocuments

    def indexing(self, stemer: Stemer, index: Index):
        text: str = self.dictInfoDocument.get("TEXT").lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        listWord = text.split()
        i: int = 0
        for word in listWord:
            i += 1
            stemerized_word = stemer.stemerize(word)
            if (not self.stop_words.Contains(stemerized_word)):
                index.Add(stemerized_word, self.id, i)
