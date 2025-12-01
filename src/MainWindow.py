import sys
import time
from PySide6 import QtCore, QtWidgets
from ui.InfoDocument import InfoDocument

from Index import Index
from Query import Query
from Soundex import Soundex
from Stemer import Stemer
from Document import Document
from StopWords import StopWords

class MainWindow(QtWidgets.QMainWindow):
    
    index: Index
    stemer: Stemer
    soundex: Soundex
    documents: dict[str, Document]
    
    def __init__(self, index: Index, stemer: Stemer, soundex: Soundex, documents: list[Document]):
        super().__init__()
        self.index = index
        self.stemer = stemer
        self.soundex = soundex
        self.documents = { d.id : d for d in documents}

        self.setWindowTitle("Moteur de recherche")
        
        self.textField = QtWidgets.QLineEdit()
        self.textField.setFocusPolicy(QtCore.Qt.ClickFocus) 

        self.queryButton = QtWidgets.QPushButton("Search")
        self.queryButton.clicked.connect(self.search)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.textField)
        layout.addWidget(self.queryButton)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.queryCorrected = QtWidgets.QLabel()
        self.nbResultDoc = QtWidgets.QLabel("Documents trouvés : 0")

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(widget)
        layout2.addWidget(self.queryCorrected)
        layout2.addWidget(self.nbResultDoc)

        widget2 = QtWidgets.QWidget()
        widget2.setLayout(layout2)

        self.setMenuWidget(widget2)

        self.resultLayout = QtWidgets.QVBoxLayout()

        widget3 = QtWidgets.QWidget()
        widget3.setLayout(self.resultLayout)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widget3)

        self.setCentralWidget(scrollArea)
    
    def search(self):
        
        while self.resultLayout.count():
            item = self.resultLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        queryText:str = self.textField.text()
        query = Query(queryText)
        listWordQuery:list[str]= query.getStemerWords(stemer)
        listCorrectedWordQuery:list[str]= query.getCorrectedWords(stemer, soundex)
        if(listWordQuery != listCorrectedWordQuery):
            queryTextCorrected:str = "Essayez avec l'orthographe :<b>"
            for i in range (0,len(listWordQuery)):
                if(listWordQuery[i] != listCorrectedWordQuery[i]):
                    queryTextCorrected += " <font style=\"color:blue;\">" + listCorrectedWordQuery[i] + "</font>"
                else:
                    queryTextCorrected += " " + listWordQuery[i]
            self.queryCorrected.setText(queryTextCorrected + "</b>")
        else:
            self.queryCorrected.setText("")
        
        startTime = time.time()
        docsFound = index.Query(listWordQuery)
        endTime = time.time()
        nbDocDisplay: int = 20
        for d, s in docsFound[:nbDocDisplay]:
            self.resultLayout.addWidget(InfoDocument(self.documents[d],listWordQuery,stemer))
        
        if len(docsFound)> nbDocDisplay:
            self.nbResultDoc.setText("Documents trouvés : "+str(len(docsFound))+ " ("+str(nbDocDisplay)+" affichés)\t Temps : "+str(endTime-startTime)[:7]+"s" )
        else:
            self.nbResultDoc.setText("Documents trouvés : "+str(len(docsFound)))
        
        if len(docsFound) == 0:
            self.resultLayout.addWidget(QtWidgets.QLabel("Aucun documents trouvés :("))



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    index_path: str = "ressources/index.bin"
    documents_dir: str = "ressources/documents"
    stemer_path: str = "ressources/stem.txt"
    stopword_path: str = "ressources/stopword.txt"
    words_path: str = "ressources/words.txt"

    stemer: Stemer = Stemer(stemer_path)
    stopwords: StopWords = StopWords(stopword_path)
    documents = sorted(Document.loadDocuments(documents_dir,stopwords), key = lambda d : d.id)
    soundex = Soundex(words_path)

    index: Index = Index.LoadFromFile(index_path)
    if index == None:
        index = Index.FromDocuments(documents, stemer)
        index.SaveToFile(index_path)

    widget = MainWindow(index,stemer,soundex,documents)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())