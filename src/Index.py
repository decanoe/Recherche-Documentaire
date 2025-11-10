from __future__ import annotations
from typing import Any

class Index:
    class WeightList:
        class Link:
            document_id: str
            nb_occurrence: int
            weight: float
            
            next_link: Index.WeightList.Link
            
            def __init__(self, document_id: str, nb_occurrence: int = 1):
                self.document_id = document_id
                self.nb_occurrence = nb_occurrence
                self.next_link = None
                
            def Add(self, document_id: str, nb_occurrence: int = 1):
                if (self.document_id == document_id):
                    self.nb_occurrence += nb_occurrence
                else:
                    if (self.next_link == None):
                        self.next_link = Index.WeightList.Link(document_id, nb_occurrence)
                    elif (document_id < self.next_link.document_id):
                        temp = self.next_link
                        self.next_link = Index.WeightList.Link(document_id, nb_occurrence)
                        self.next_link.next_link = temp
                    else:
                        self.next_link.Add(document_id, nb_occurrence)
                
            def RecomputeWeights(self, total_occurence: int):
                self.weight = self.nb_occurrence
                
                if (self.next_link != None):
                    self.next_link.RecomputeWeights(total_occurence)
        
        root: Index.WeightList.Link
        count: int
        
        def __init__(self):
            self.root = None
            self.count = 0
        
        def Add(self, document_id: str, nb_occurrence: int = 1):
            if self.root == None:
                self.root = Index.WeightList.Link(document_id, nb_occurrence)
            else:
                self.root.Add(document_id, nb_occurrence)
            self.count += nb_occurrence
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
            self.keys = self.keys[:self.min_count - 1]
            self.children = self.children[:self.min_count]
            
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
                if (self.keys[i] == key):
                    return self.children[i]
                return default
            return self.children[i].Get(key)
        def GetOrSetDefault(self, key: str, default: Index.WeightList = None) -> Index.WeightList:
            result = self.Get(key)
            if (result == None):
                self.Add(default)
                return default
            return result
        
        def __str__(self, prefix = "") -> str:
            out: str = prefix + "("
            if (self.Size() != 0):
                for i in range(self.Size() - 1):
                    if (self.IsLeaf()):
                        out += str(self.children[i]) + " [" + self.keys[i] + "] "
                    else:
                        out += "\n" + self.children[i].__str__(prefix + "    ") + "\n" + prefix + "    [" + self.keys[i] + "]"
                if (self.IsLeaf()):
                    out += str(self.children[self.Size() - 1])
                else:
                    out += "\n" + self.children[self.Size() - 1].__str__(prefix + "    ")
            
            if (self.IsLeaf()):
                return out + ")"
            else:
                return out + "\n" + prefix + ")"

    tree: Index.Tree
    
    def __init__(self):
        self.tree = Index.Tree()
    
    def Add(self, word: str, document_id: str):
        self.tree.GetOrSetDefault(word, Index.WeightList()).Add(document_id)