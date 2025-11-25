class StopWords:
    word_list: list[str]
    
    def __init__(self, path: str):
        with open(path, "r") as file:
            self.word_list = [w.strip() for w in file.readlines() if w.strip() != ""]
    
    def Contains(self, word: str) -> bool:
        return word in self.word_list
