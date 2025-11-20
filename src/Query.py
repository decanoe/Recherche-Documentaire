from Stemer import Stemer
from Soundex import Soundex
import re


class Query:
    queryWords: list[str]

    def __init__(self, content: str):
        self.queryWords = (re.sub(r"[^a-z0-9\s*]", " ", content.lower())).split()

    def getStemerWords(self, stemer: Stemer):
        wordList: list[str] = []
        for word in self.queryWords:
            wordList.append(stemer.stemerize(word))
        return wordList

    def getCorrectedWords(self, stemer: Stemer, soundex: Soundex):
        wordList: list[str] = []
        for word in self.queryWords:
            if "*" in word:
                wordList.append(word)
            elif stemer.isStemerizable(word):
                wordList.append(stemer.stemerize(word))
            else:
                listSoundexWord: list[str] = soundex.dictSoundex.get(
                    soundex.soundexerize(word)
                )
                listCost: list[str] = []
                for soundexWord in listSoundexWord:
                    cost: int = 0
                    for i in range(1, len(soundexWord) - 1):
                        for j in range(1, len(word) - 1):
                            if soundexWord[i - 1 : i + 1] == word[j - 1 : j + 1]:
                                cost += 1
                    listCost.append(cost)
                wordList.append(
                    stemer.stemerize(listSoundexWord[listCost.index(max(listCost))])
                )
        return wordList
