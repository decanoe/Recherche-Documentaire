from __future__ import annotations
from typing import Any

class Index:
    class Node:
        min_count: int
        max_count: int
        
        keys: list[str]
        leaf: bool
        root: bool
        children: list[Index.Node | Any]
        
        def __init__(self, min_count: int = 2, max_count: int = 4, leaf: bool = True, root: bool = True, keys: list[str] = [], children: list[Index.Node | Any] = []):
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
        
        def Split(self) -> tuple[str, Index.Node]:
            node: Index.Node = Index.Node(self.min_count, self.max_count, self.leaf, False, self.keys[self.min_count:], self.children[self.min_count:])
            key: str = self.keys[self.min_count - 1]
            self.keys = self.keys[:self.min_count - 1]
            self.children = self.children[:self.min_count]
            
            return (key, node)
            
        '''
        fonction Inserer(x,c)
            n = nombre de clefs du noeud x
            Soit i tel que x.clef[i] > c ou i >= n
            Si x est une feuille :
                Inserer c dans x.clef a la i-ieme place
            Sinon:
                Si x.fils[i] est complet:
                    Scinder x.fils[i]
                    Si c > x.clef[i]:
                        i := i+1
                    FinSi
                FinSi
                Inserer(x.fils[i],c)
            FinSi
        FinFonction
        '''
        def _Add(self, key: str, value: Any):
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
        def _RootAdd(self, key: str, value: Any):
            self._Add(key, value)
            
            if (self.IsFull()):
                middle_key, right_node = self.Split()
                left_node = Index.Node(self.min_count, self.max_count, self.leaf, False, self.keys, self.children)
                
                self.children = [left_node, right_node]
                self.keys = [middle_key]
                self.leaf = False
                    
        def Add(self, key: str, value: Any):
            if (self.root):
                return self._RootAdd(key, value)
            else:
                return self._Add(key, value)
        
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

    def __init__():
        pass
    
    def Add(word: str, document_id: str):
        pass