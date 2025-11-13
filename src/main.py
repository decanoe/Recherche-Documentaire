from Document import Document
from Stemer import Stemer
from Index import Index

listDocuments = Document.loadDocuments("ressources/documents")
stemer = Stemer("ressources/stem.txt")
index = Index()
for document in listDocuments:
    document.indexing(stemer, index)
