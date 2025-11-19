from Stemer import Stemer
import re


class Soundex:
    dictAlphabetCode: dict[str, int]
    dictSoundex: dict[str, list[str]]

    def __init__(self, stemer: Stemer):
        self.dictAlphabetCode = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 0,
            "f": 1,
            "g": 2,
            "h": 0,
            "i": 0,
            "j": 2,
            "k": 2,
            "l": 4,
            "m": 5,
            "n": 5,
            "o": 0,
            "p": 1,
            "q": 2,
            "r": 6,
            "s": 2,
            "t": 3,
            "u": 0,
            "v": 1,
            "w": 0,
            "x": 2,
            "y": 0,
            "z": 2,
        }
        self.dictSoundex = {}
        self.createSoundex(stemer)

    def createSoundex(self, stemer: Stemer):
        for word in stemer.dictStem.keys():
            soundexCode: str = self.soundexerize(word)
            if self.dictSoundex.get(soundexCode) == None:
                self.dictSoundex[soundexCode] = []
            self.dictSoundex[soundexCode].append(word)

    def soundexerize(self, word: str) -> str:
        if re.fullmatch(r"[a-zA-Z]+", word):
            tempSoundexCode: str = word[0].lower()
            for i in range(1, len(word)):
                tempSoundexCode += str(self.dictAlphabetCode.get(word[i].lower()))
            soundexCode: str = tempSoundexCode[0]
            for i in range(1, len(tempSoundexCode) - 1):
                if tempSoundexCode[i] != tempSoundexCode[i + 1]:
                    soundexCode += tempSoundexCode[i]
            soundexCode = soundexCode.replace("0", "")
            if len(soundexCode) >= 4:
                soundexCode = soundexCode[:4]
            else:
                while len(soundexCode) < 4:
                    soundexCode += str(0)
            return soundexCode
