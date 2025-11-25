import sys
from PySide6 import QtCore, QtWidgets, QtGui

from Index import Index
from Query import Query
from Soundex import Soundex
from Stemer import Stemer
from Document import Document

class MyWidget(QtWidgets.QWidget):
    # root: Tk
    # global_frame: ttk.Frame
    # search_frame: ttk.Frame
    # result_frame: ttk.Frame
    
    # results: list[ttk.Frame]
    
    # query_text: StringVar
    # query: Query
    
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

        self.query_label = QtWidgets.QLabel("Query:", alignment=QtCore.Qt.AlignRight)
        self.query_button = QtWidgets.QPushButton("Search")
        self.query_button.clicked.connect(self.ApplyQuery)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        
    def ApplyQuery(self):
        self.query = Query(self.query_text.get())
        
        print("Query: ", self.query.getCorrectedWords(self.stemer, self.soundex))
        
        # for result in self.results:
        #     result.destroy()
        # i = 0
        # for d, s in index.Query(self.query.getCorrectedWords(stemer, soundex))[:10]:
        #     result = ttk.Frame(self.result_frame, padding=10, borderwidth=2, relief=GROOVE)
            
        #     result.grid(column=0, row=i)
        #     ttk.Label(result, text=f"{d} \twith a score of {round(s,3)}").grid(column=0, row=0)
            
        #     text_area = scrolledtext.ScrolledText(result)
        #     text_area.grid(column = 0, row=1)
        #     text_area.insert(INSERT, self.documents[d].dictInfoDocument["TEXT"])
        #     text_area.config(state=DISABLED)
            
        #     i += 1



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())