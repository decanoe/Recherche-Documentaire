from Document import Document
from Stemer import Stemer
from Index import Index

listDocuments = Document.loadDocuments("ressources/documents")
stemer = Stemer("ressources/stem.txt")
index = Index()
for document in listDocuments[:10]:
    document.indexing(stemer, index)
index.RecomputeWeights()

for d, s in index.Query(["new", "york"]):
    print(f"{d} \twith a score of {s}")
