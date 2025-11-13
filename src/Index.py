from __future__ import annotations
from typing import Any
import math

class Index:
    class WeightList:
        class Weight:
            document_id: str
            nb_occurrence: int
            weight: float
            
            def __init__(self, document_id: str, nb_occurrence: int = 0):
                self.document_id = document_id
                self.nb_occurrence = nb_occurrence
                self.weight = 1
                
            def Add(self, nb_occurrence: int = 1):
                self.nb_occurrence += nb_occurrence
                
            def RecomputeWeights(self, idf: float, document_lengths: dict[str, float]):
                if (self.nb_occurrence == 0):
                    self.weight = 0
                    return

                self.weight = (1 + math.log10(self.nb_occurrence)) * idf
                document_lengths[self.document_id] += self.weight * self.weight
            
            def __str__(self) -> str:
                return f"({self.document_id}: {self.nb_occurrence}/{self.weight})"
            
        word: str
        elements: list[Index.WeightList.Weight]
        idf: float
        
        def __init__(self, word: str):
            self.word = word
            self.elements = []
        
        def Get(self, document_id: str) -> Index.WeightList.Weight:
            for w in self.elements:
                if (document_id < w.document_id):
                    return None
                if (document_id == w.document_id):
                    return w
        def GetOrSet(self, document_id: str) -> Index.WeightList.Weight:
            i: int = 0
            for w in self.elements:
                if (document_id < w.document_id):
                    e = Index.WeightList.Weight(document_id, 0)
                    self.elements.insert(i, e)
                    return e
                if (document_id == w.document_id):
                    return w
                i += 1
            
            e = Index.WeightList.Weight(document_id, 0)
            self.elements.append(e)
            return e
        def Add(self, document_id: str, nb_occurrence: int = 1):
            self.GetOrSet(document_id).Add(nb_occurrence)
    
        def RecomputeWeights(self, document_count: int, document_lengths: dict[str, float]):
            self.idf = math.log10(document_count / len(self.elements))
            for w in self.elements:
                w.RecomputeWeights(self.idf, document_lengths)
        
        def __str__(self, full: bool = True) -> str:
            if (full):
                return f"{self.word}: (" + ", ".join([str(e) for e in self.elements]) + ")"
            return f"(WeightList for \"{self.word}\")"

    class Tree:
        min_count: int
        max_count: int
        
        keys: list[str]
        leaf: bool
        root: bool
        children: list[Index.Tree | Index.WeightList]
        
        def __init__(self, min_count: int = 2, max_count: int = 4, leaf: bool = True, root: bool = True, keys: list[str] = [], children: list[Index.Tree | Any] = []):
            self.leaf = leaf
            self.root = root
            self.min_count = min_count
            self.max_count = max_count
            self.keys = keys
            self.children = children
        
        def IsLeaf(self) -> bool:
            return self.leaf
        def IsRoot(self) -> bool:
            return self.root
        def IsFull(self) -> bool:
            return len(self.children) == self.max_count
        def Size(self) -> bool:
            return len(self.children)
        
        def Split(self) -> tuple[str, Index.Tree]:
            node: Index.Tree = Index.Tree(self.min_count, self.max_count, self.leaf, False, self.keys[self.min_count:], self.children[self.min_count:])
            key: str = self.keys[self.min_count - 1]
            self.children = self.children[:self.min_count]
            if (self.IsLeaf()):
                self.keys = self.keys[:self.min_count]
            else:
                self.keys = self.keys[:self.min_count - 1]
            return (key, node)
            
        def _Add(self, key: str, value: Index.WeightList):
            i: int = 0
            while i < len(self.keys) and key > self.keys[i]:
                i += 1
            
            if (self.leaf):
                self.keys.insert(i, key)
                self.children.insert(i, value)
                return
            else:
                if (self.children[i].IsFull()):
                    middle_key, right_node = self.children[i].Split()
                    self.children.insert(i + 1, right_node)
                    self.keys.insert(i, middle_key)
                    if (key > self.keys[i]):
                        i += 1
                return self.children[i]._Add(key, value)
        def _RootAdd(self, key: str, value: Index.WeightList):
            self._Add(key, value)
            
            if (self.IsFull()):
                middle_key, right_node = self.Split()
                left_node = Index.Tree(self.min_count, self.max_count, self.leaf, False, self.keys, self.children)
                
                self.children = [left_node, right_node]
                self.keys = [middle_key]
                self.leaf = False
        def Add(self, key: str, value: Index.WeightList):
            if (self.root):
                return self._RootAdd(key, value)
            else:
                return self._Add(key, value)
        
        def Get(self, key: str, default: Index.WeightList = None) -> Index.WeightList:
            i: int = 0
            while i < len(self.keys) and key > self.keys[i]:
                i += 1
            
            if (self.IsLeaf()):
                if (i == len(self.keys)):
                    return default
                if (self.keys[i] == key):
                    return self.children[i]
                return default
            return self.children[i].Get(key)
        def GetOrSetDefault(self, key: str, default: Index.WeightList = None) -> Index.WeightList:
            result = self.Get(key)
            if (result == None):
                self.Add(key, default)
                return default
            return result
        
        def RecomputeWeights(self, document_count: int, document_lengths: dict[str, float]):
            for child in self.children:
                child.RecomputeWeights(document_count, document_lengths)
        
        def __str__(self, prefix = "") -> str:
            out: str = prefix + "("
            if (self.Size() != 0):
                for i in range(self.Size() - 1):
                    if (self.IsLeaf()):
                        out += f"\n{prefix}    " + str(self.children[i]) + f"\n{prefix}    [" + self.keys[i] + "] "
                    else:
                        out += "\n" + self.children[i].__str__(prefix + "    ") + f"\n{prefix}    [" + self.keys[i] + "]"
                if (self.IsLeaf()):
                    out += f"\n{prefix}    " + str(self.children[self.Size() - 1])
                else:
                    out += "\n" + self.children[self.Size() - 1].__str__(prefix + "    ")
            
            return out + "\n" + prefix + ")"

    tree: Index.Tree
    document_lengths: dict[str, float]
    
    def __init__(self):
        self.tree = Index.Tree()
        self.document_lengths = {}
    def Add(self, word: str, document_id: str):
        self.tree.GetOrSetDefault(word, Index.WeightList(word)).Add(document_id)
        self.document_lengths[document_id] = -1
    def RecomputeWeights(self, document_count: int):
        for key in self.document_lengths.keys():
            self.document_lengths[key] = 0
        
        self.tree.RecomputeWeights(document_count, self.document_lengths)
        
        for key, length in self.document_lengths.items():
            self.document_lengths[key] = math.sqrt(length)
    
    def Query(self, words: list[str]) -> list[tuple[str, float]]:
        word_occ: dict[str, int] = {}
        for w in words:
            word_occ[w] = word_occ.get(w, 0) + 1
        
        # ================ QUERY VECTOR CONSTRUCTION ========================
        query_vector: dict[str, float] = {}
        query_length: float = 0
        for word, count in word_occ.items():
            query_vector[word] = (1 + math.log10(count))
            query_length += query_vector[word] * query_vector[word]
            
        query_length = math.sqrt(query_length)
        for word in query_vector.keys():
            query_vector[word] /= query_length
        
        # ================ SCORE COMPUTATION ========================
        scores: dict[str, float] = {}
        
        for word, value in query_vector.items():
            weight_list: Index.WeightList = self.tree.Get(word)
            if (weight_list != None):
                for weight in weight_list.elements:
                    v: float = weight.weight * value
                    scores[weight.document_id] = scores.get(weight.document_id, 0) + v
        
        for key in scores.keys():
            if (self.document_lengths[key] != 0):
                scores[key] /= self.document_lengths[key]
        
        result = [(key, score) for key, score in scores.items()]
        result.sort(key=lambda s: s[1], reverse=True)
        return result