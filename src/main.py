from Document import Document
from Stemer import Stemer
from Index import Index
from Soundex import Soundex
from Query import Query

index_path: str = "ressources/index.bin"
documents_dir: str = "ressources/documents"
stemer_path: str = "ressources/stem.txt"

stemer: Stemer = Stemer(stemer_path)

index: Index = Index.LoadFromFile(index_path)
if index == None:
    index = Index.FromDocuments(Document.loadDocuments(documents_dir), stemer)
    index.SaveToFile(index_path)

soundex = Soundex(stemer)

query = Query("New York*!")
print(query.getCorrectedWords(stemer, soundex))
for d, s in index.Query(query.getCorrectedWords(stemer, soundex))[:10]:
    print(f"{d} \twith a score of {s}")
