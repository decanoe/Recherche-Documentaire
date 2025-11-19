from Document import Document
from Stemer import Stemer
from Index import Index
from Query import Query

index_path: str = "ressources/index.bin"
documents_dir: str = "ressources/documents"
stemer_path: str = "ressources/stem.txt"

stemer: Stemer = Stemer(stemer_path)

index: Index = Index.LoadFromFile(index_path)
if (index == None):
    index = Index.FromDocuments(Document.loadDocuments(documents_dir), stemer)
    index.SaveToFile(index_path)

query = Query("New York!")
print(query.getStemerWords(stemer))
for d, s in index.Query(query.getStemerWords(stemer)):
    print(f"{d} \twith a score of {s}")
