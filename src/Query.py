from Stemer import Stemer
import re


class Query:
    content: str

    def __init__(self, content: str):
        self.content = content

    def getStemerWords(self, stemer: Stemer):
        wordList: list[str] = []
        query: str = self.content.lower()
        query = re.sub(r"[^a-z0-9\s]", " ", query)
        for word in query.split():
            wordList.append(stemer.stemerize(word))
        return wordList
