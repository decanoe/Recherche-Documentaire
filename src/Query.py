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
                trigrams: list[str] = self.getTrigrams(word)
                for soundexWord in listSoundexWord:
                    sondex_trigrams: list[str] = self.getTrigrams(soundexWord)
                    listCost.append(self.countIntersectionCardinal(trigrams, sondex_trigrams) / self.countUnionCardinal(trigrams, sondex_trigrams))
                wordList.append(
                    stemer.stemerize(listSoundexWord[listCost.index(max(listCost))])
                )
        return wordList

    def getTrigrams(self, word: str) -> list[str]:
        output: list[str] = []
        for i in range(1, len(word) - 1):
            if word[i - 1 : i + 1] not in output:
                output.append(word[i - 1 : i + 1])
        return output
    def countIntersectionCardinal(self, trigrams1: list[str], trigrams2: list[str]) -> list[str]:
        count: int = 0
        for t in trigrams2:
            if t in trigrams1:
                count += 1
        return count
    def countUnionCardinal(self, trigrams1: list[str], trigrams2: list[str]) -> list[str]:
        count: int = 0
        for t in trigrams2:
            if t not in trigrams1:
                count += 1
        return count + len(trigrams1)