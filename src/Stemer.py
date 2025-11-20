class Stemer:
    wordsListByDocument: dict[str, list[str]]
    dictStem: dict[str, str]

    def __init__(self, stemFile: str):
        self.wordsListByDocument = {}
        self.dictStem = {}
        self.readStem(stemFile)

    def readStem(self, stemFile: str) -> dict[list[str]]:
        with open(stemFile, "r") as f:
            lines = f.readlines()[1:]
            for line in lines:
                listWord: list[str] = line.split("|")
                root: str = listWord[0].strip()
                listWord = [word.strip() for word in listWord[1].split()]
                for word in listWord:
                    self.dictStem[word] = root

    def stemerize(self, word) -> str:
        return self.dictStem.get(word, word)

    def isStemerizable(self, word) -> bool:
        return word in self.dictStem
