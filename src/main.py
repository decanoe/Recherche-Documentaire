from Document import Document
from Stemer import Stemer
from Index import Index
from Query import Query

listDocuments = Document.loadDocuments("ressources/documents")
stemer = Stemer("ressources/stem.txt")
index = Index()
for document in listDocuments[:10]:
    document.indexing(stemer, index)
index.RecomputeWeights()

query = Query("New York!")
print(query.getStemerWords(stemer))
for d, s in index.Query(query.getStemerWords(stemer)):
    print(f"{d} \twith a score of {s}")
