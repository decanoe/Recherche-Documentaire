from Document import Document
from Stemer import Stemer
from Index import Index
from Soundex import Soundex
from StopWords import StopWords
from Query import Query

index_path: str = "ressources/index.bin"
documents_dir: str = "ressources/documents"
stemer_path: str = "ressources/stem.txt"
stopword_path: str = "ressources/stopword.txt"
words_path: str = "ressources/words.txt"

stemer: Stemer = Stemer(stemer_path)
stopwords: StopWords = StopWords(stopword_path)
soundex = Soundex(words_path)

index: Index = Index.LoadFromFile(index_path)
documents = Document.loadDocuments(documents_dir, stopwords)
documents = sorted(documents, key = lambda d : d.id)

if index == None:
    index = Index.FromDocuments(documents, stemer)
    index.SaveToFile(index_path)
# index.CreateStopWordList(stopword_path, 0.1)

query = Query("New York*!")
print(query.getCorrectedWords(stemer, soundex))
for d, s in index.Query(query.getCorrectedWords(stemer, soundex))[:10]:
    print(f"{d} \twith a score of {s}")

print(index.QueryWords(query.getCorrectedWords(stemer, soundex)))