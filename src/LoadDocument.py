class LoadDocument:
    listDocuments: list[dict[str, str]]

    def __init__(self):
        self.listDocuments = []

    def loadDocuments(self, file):
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
                    self.listDocuments.append(document)
