from Document import Document
from Stemer import Stemer
from PySide6 import QtCore, QtWidgets
import re


class InfoDocument(QtWidgets.QGroupBox):

    def __init__(self, document:Document,query:list[str], stemer:Stemer):
        super().__init__(document.dictInfoDocument["HEAD"])
        
        groupLayout = QtWidgets.QVBoxLayout()
        text: str = document.dictInfoDocument["TEXT"].strip()
        copyText = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        copyText = copyText.strip()
        exploredWords = []
        queryRegex = [w.replace("*", ".*") for w in query if "*" in w]
        for word in copyText.split():
            if word not in exploredWords:
                exploredWords.append(word)
                if stemer.stemerize(word.lower()) in query:
                    text = re.sub(r"\b"+word+r"\b","<b style=\"color:red;\">"+word+"</b>", text)
                else:
                    for regex in queryRegex:
                        if re.fullmatch(regex, word.lower()):
                            text = re.sub(r"\b"+word+r"\b","<b style=\"color:red;\">"+word+"</b>", text)


        label = QtWidgets.QLabel("<font>"+text.replace(".\n",".<br/>")+"</font>")
        label.setWordWrap(True)
        groupLayout.addWidget(label)
        self.setLayout(groupLayout)

        




