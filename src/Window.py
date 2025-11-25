from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

from Index import Index
from Query import Query
from Soundex import Soundex
from Stemer import Stemer
from Document import Document

class Window:
    root: Tk
    global_frame: ttk.Frame
    search_frame: ttk.Frame
    result_frame: ttk.Frame
    
    results: list[ttk.Frame]
    
    query_text: StringVar
    query: Query
    
    index: Index
    stemer: Stemer
    soundex: Soundex
    documents: dict[str, Document]
    
    def __init__(self, index: Index, stemer: Stemer, soundex: Soundex, documents: list[Document]):
        self.index = index
        self.stemer = stemer
        self.soundex = soundex
        self.documents = { d.id : d for d in documents}
        
        self.root = Tk()
        self.global_frame = ttk.Frame(self.root, padding=10)
        self.global_frame.grid()
        
        self.search_frame = ttk.Frame(self.global_frame, padding=10, borderwidth=2, relief=GROOVE)
        self.search_frame.grid(column=0, row=0)
        
        self.result_frame = ttk.Frame(self.global_frame, padding=10)
        self.result_frame.grid(column=0, row=1)

        ttk.Label(self.search_frame, text="Query:").grid(column=0, row=0)

        self.query_text = StringVar()
        self.query_text.set("New Yor*!")
        Entry(self.search_frame, textvariable=self.query_text, width=30).grid(column=1, row=0)

        ttk.Button(self.search_frame, text="Search", command=self.ApplyQuery).grid(column=2, row=0)
        self.results = []

        ttk.Button(self.result_frame, text="Quit", command=self.root.destroy).grid(column=0, row=0)
        self.root.mainloop()
    
    def ApplyQuery(self):
        self.query = Query(self.query_text.get())
        
        print("Query: ", self.query.getCorrectedWords(self.stemer, self.soundex))
        
        for result in self.results:
            result.destroy()
        i = 0
        for d, s in index.Query(self.query.getCorrectedWords(stemer, soundex))[:10]:
            result = ttk.Frame(self.result_frame, padding=10, borderwidth=2, relief=GROOVE)
            
            result.grid(column=0, row=i)
            ttk.Label(result, text=f"{d} \twith a score of {round(s,3)}").grid(column=0, row=0)
            
            text_area = scrolledtext.ScrolledText(result)
            text_area.grid(column = 0, row=1)
            text_area.insert(INSERT, self.documents[d].dictInfoDocument["TEXT"])
            text_area.config(state=DISABLED)
            
            i += 1

index_path: str = "ressources/index.bin"
documents_dir: str = "ressources/documents"
stemer_path: str = "ressources/stem.txt"

stemer: Stemer = Stemer(stemer_path)
documents = sorted(Document.loadDocuments(documents_dir), key = lambda d : d.id)
soundex = Soundex(stemer)

index: Index = Index.LoadFromFile(index_path)
if index == None:
    index = Index.FromDocuments(documents[:10], stemer)
    index.SaveToFile(index_path)

window: Window = Window(index, stemer, soundex, documents)