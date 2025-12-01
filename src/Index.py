from __future__ import annotations
from typing import Any
import math
import pickle
import os

from Stemer import Stemer


class Index:
    class WeightList:
        class Weight:
            positions_count: int
            weight: float

            def __init__(self):
                self.positions_count = 0
                self.weight = 1

            def Add(self, position: int):
                self.positions_count += 1

            def RecomputeWeights(self, idf: float):
                if self.positions_count == 0:
                    self.weight = 0
                    return
                self.weight = (1 + math.log10(self.positions_count)) * idf

            def __str__(self) -> str:
                return f"({self.positions_count}/{round(self.weight,3)})"

        _word: str
        _elements: dict[str, Index.WeightList.Weight]
        _idf: float

        def __init__(self, word: str):
            self._word = word
            self._elements = {}

        def _Get(self, document_id: str) -> Index.WeightList.Weight:
            return self._elements.get(document_id, Index.WeightList.Weight())
        def _GetOrSet(self, document_id: str) -> Index.WeightList.Weight:
            if document_id not in self._elements:
                self._elements[document_id] = Index.WeightList.Weight()
            return self._elements[document_id]
        def Add(self, document_id: str, position: int):
            self._GetOrSet(document_id).Add(position)

        def RecomputeWeights(self, document_count: int, document_lengths: dict[str, float]):
            self._idf = math.log10(document_count / len(self._elements))
            for d, w in self._elements.items():
                w.RecomputeWeights(self._idf)
                document_lengths[d] += w.weight * w.weight

        def GetIDF(self) -> float:
            return self._idf
        def GetDocumentWeights(self) -> list[tuple[str, float]]:
            return [(d, e.weight) for d, e in self._elements.items()]
        def IsEmpty(self) -> bool:
            return len(self._elements) == 0

        def __str__(self, full: bool = True) -> str:
            if full:
                return (
                    f"{self._word}: ("
                    + ", ".join([d + ":" + str(e) for d, e in self._elements.items()])
                    + ")"
                )
            return f'(WeightList for "{self._word}")'
    
    class Tree:
        min_count: int
        max_count: int

        keys: list[str]
        leaf: bool
        root: bool
        children: list[Index.Tree | Index.WeightList | str]

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
            self.children = self.children[: self.min_count]
            if self.IsLeaf():
                self.keys = self.keys[: self.min_count]
            else:
                self.keys = self.keys[: self.min_count - 1]
            return (key, node)

        def greater(self, key: str, to_key: str):
            if key[-1] == "*":
                return key[:-1] > to_key
            return key > to_key
        def lower_equal(self, key: str, to_key: str):
            if key[-1] == "*":
                return key[:-1] <= to_key
            return key <= to_key
        def equal(self, key: str, to_key: str):
            if key[-1] == "*" and to_key.startswith(key[:-1]):
                return True
            return key == to_key

        def _Add(self, key: str, value: Index.WeightList) -> Index.WeightList:
            i: int = 0
            while i < len(self.keys) and self.greater(key, self.keys[i]):
                i += 1

            if self.leaf:
                if i == len(self.keys):
                    self.keys.append(key)
                    self.children.append(value)
                    return value
                if self.equal(key, self.keys[i]):
                    return self.children[i]
                self.keys.insert(i, key)
                self.children.insert(i, value)
                return value
            else:
                if self.children[i].IsFull():
                    middle_key, right_node = self.children[i].Split()
                    self.children.insert(i + 1, right_node)
                    self.keys.insert(i, middle_key)
                    if self.greater(key, self.keys[i]):
                        i += 1
                return self.children[i]._Add(key, value)
        def _RootAdd(self, key: str, value: Index.WeightList) -> Index.WeightList:
            result = self._Add(key, value)

            if self.IsFull():
                middle_key, right_node = self.Split()
                left_node = Index.Tree(self.min_count, self.max_count, self.leaf, False, self.keys, self.children)

                self.children = [left_node, right_node]
                self.keys = [middle_key]
                self.leaf = False
            return result
        def Add(self, key: str, value: Index.WeightList) -> Index.WeightList:
            if self.root:
                return self._RootAdd(key, value)
            else:
                return self._Add(key, value)

        def _GetSingle(self, key: str) -> Index.WeightList | str:
            i: int = 0
            while i < len(self.keys) and self.greater(key, self.keys[i]):
                i += 1

            if self.IsLeaf():
                if i == len(self.keys):
                    return None
                if self.equal(key, self.keys[i]):
                    return self.children[i]
                return None
            return self.children[i]._GetSingle(key)
        def _GetMultiple(self, key: str) -> list[Index.WeightList | str]:
            i: int = 0
            while i < len(self.keys) and self.greater(key, self.keys[i]):
                i += 1

            result = []
            if self.IsLeaf():
                while i < len(self.keys) and self.equal(key, self.keys[i]):
                    result.append(self.children[i])
                    i += 1
                return result
            else:
                while i < len(self.keys) and self.equal(key, self.keys[i]):
                    result += self.children[i]._GetMultiple(key)
                    i += 1
                result += self.children[i]._GetMultiple(key)
                return result
        def Get(self, key: str) -> list[Index.WeightList]:
            if (not self.IsRoot()):
                raise Exception("Get must be called on the root of the tree")
            
            if key[-1] == "*":
                result = []
                potential_results = self._GetMultiple(key)
                while len(potential_results) != 0:
                    temp = potential_results.pop()
                    if isinstance(temp, str):
                        temp = self._GetSingle(temp)
                    if (temp not in result):
                        result.append(temp)
                return result
            else:
                result = self._GetSingle(key)
                if isinstance(result, str):
                    result = self._GetSingle(result)
                return [] if result == None else [result]
        
        def RecomputeWeights(self, document_count: int, document_lengths: dict[str, float]):
            for child in self.children:
                if isinstance(child, str):
                    continue
                child.RecomputeWeights(document_count, document_lengths)
        
        def __str__(self, prefix="") -> str:
            out: str = prefix + "("
            if self.Size() != 0:
                for i in range(self.Size() - 1):
                    if self.IsLeaf():
                        out += (
                            f"\n{prefix}    "
                            + str(self.children[i])
                            + f"\n{prefix}    ["
                            + self.keys[i]
                            + "] "
                        )
                    else:
                        out += (
                            "\n"
                            + self.children[i].__str__(prefix + "    ")
                            + f"\n{prefix}    ["
                            + self.keys[i]
                            + "]"
                        )
                if self.IsLeaf():
                    out += f"\n{prefix}    " + str(self.children[self.Size() - 1])
                else:
                    out += "\n" + self.children[self.Size() - 1].__str__(
                        prefix + "    "
                    )

            return out + "\n" + prefix + ")"

    tree: Index.Tree
    document_lengths: dict[str, float]

    def __init__(self):
        self.tree = Index.Tree()
        self.document_lengths = {}

    def LoadFromFile(index_path: str) -> Index:
        if os.path.exists(index_path):
            print("\033[2KLoading index", end="\r")
            index = pickle.load(open(index_path, "rb"))
            print("\033[2K", end="\r")
            return index
        else:
            return None
    def FromDocuments(listDocuments: list, stemer: Stemer) -> Index:
        index: Index = Index()

        i = 0
        for document in listDocuments:
            document.indexing(stemer, index)
            i += 1
            print(
                f"\033[2Kindexing document {i}/{len(listDocuments)} ["
                + "█" * (round(i / len(listDocuments) * 10))
                + " " * (10 - round(i / len(listDocuments) * 10))
                + "]",
                end="\r",
            )
        index.RecomputeWeights()
        print("\033[2Kindexing completed")
        return index
    def SaveToFile(self, index_path: str) -> Index:
        pickle.dump(self, open(index_path, "wb"))
    def CreateStopWordList(self, index_path: str, threshold: float):
        with open(index_path, "w") as file:
            nodes: list[Index.Tree | str | Index.WeightList] = [self.tree]
            
            while len(nodes) != 0:
                node = nodes.pop()
                
                if (isinstance(node, Index.Tree)):
                    for child in node.children:
                        nodes.append(child)
                if (isinstance(node, Index.WeightList)):
                    if (node.GetIDF() < threshold):
                        file.write(node._word.removesuffix("$") + "\n")

    def Add(self, word: str, document_id: str, position: int):
        word += "$"
        node = self.tree.Add(word, Index.WeightList(word))
        if (node.IsEmpty()):
            for i in range(len(word)):
                rotated_word = self.Rotate(word, i)
                self.tree.Add(rotated_word, word)
        node.Add(document_id, position)
        self.document_lengths[document_id] = -1
    def Get(self, word: str) -> list[Index.WeightList]:
        return self.tree.Get(word)

    def RecomputeWeights(self):
        for key in self.document_lengths.keys():
            self.document_lengths[key] = 0

        self.tree.RecomputeWeights(len(self.document_lengths), self.document_lengths)

        for key, length in self.document_lengths.items():
            self.document_lengths[key] = math.sqrt(length)

    def Rotate(self, word: str, amount: int = 1) -> str:
        return word[amount:] + word[:amount]
    def PrepareWordForQuery(self, word: str) -> str:
        count: int = word.count("*")

        if count == 0:
            return word + "$"
        if count > 2:
            raise Exception("Impossible d'utiliser plus de 2 caractères joker dans le même mot !")

        if count == 2 and word[0] == "*" and word[-1] == "*":
            return word[1:]
        if count == 2:
            raise Exception("Impossible d'utiliser 2 caractères joker dans le même mot s'ils ne sont pas au début et à la fin !")
        if word[0] == "*":
            return word[1:] + "$*"
        if word[-1] == "*":
            return "$" + word[:-1] + "*"

        return word.split("*")[-1] + "$" + word.split("*")[0] + "*"
    def Query(self, words: list[str]) -> list[tuple[str, float]]:
        word_occ: dict[str, int] = {}
        for w in words:
            if (w == "*" or w == "**"):
                continue
            new_w: str = self.PrepareWordForQuery(w)
            word_occ[new_w] = word_occ.get(new_w, 0) + 1

        # ================ QUERY VECTOR CONSTRUCTION ========================
        query_vector: dict[str, float] = {}
        query_length: float = 0
        for word, count in word_occ.items():
            query_vector[word] = 1 + math.log10(count)
            query_length += query_vector[word] * query_vector[word]

        query_length = math.sqrt(query_length)
        for word in query_vector.keys():
            query_vector[word] /= query_length

        # ================ SCORE COMPUTATION ========================
        scores: dict[str, float] = {}

        for word, value in query_vector.items():
            for weight_list in self.Get(word):
                for document_id, weight in weight_list.GetDocumentWeights():
                    v: float = weight * value
                    scores[document_id] = scores.get(document_id, 0) + v

        for key in scores.keys():
            if self.document_lengths[key] != 0:
                scores[key] /= self.document_lengths[key]

        result = [(key, score) for key, score in scores.items()]
        result.sort(key=lambda s: s[1], reverse=True)
        return result
    def QueryWords(self, words: list[str]) -> list[str]:
        word_occ: dict[str, int] = {}
        for w in words:
            if (w == "*" or w == "**"):
                continue
            new_w: str = self.PrepareWordForQuery(w)
            word_occ[new_w] = word_occ.get(new_w, 0) + 1

        result = []
        for word in word_occ.keys():
            for weight_list in self.Get(word):
                if (weight_list._word not in result):
                    result.append(weight_list._word)
        return result