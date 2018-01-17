from Node import Node, Leaf
from Rules import AbstractRule, ConstructorRule, UnionRule, ProductRule, ConstantRule, SingletonRule, EpsilonRule, Union, Prod, Singleton, Epsilon, NonTerm

def size(tree):
    if tree.is_leaf():
        return 1
    return size(tree.left()) + size(tree.right())


def invert_union_tree(obj):
    if obj.is_leaf():
        return 1
    return 0


def invert_node(obj):
    return obj.left(), obj.right()


def size_fibo(str):
    return len(str)


def inv_union_fibo_1(obj):
    if (obj == ""):
        return 0
    return 1


def inv_union_fibo_2(obj):
    if (obj[0] == "A"):
        return 0
    return 1


def inv_union_fibo_3(obj):
    if (obj == "B"):
        return 0
    return 1


def inv_prod_fibo_1(obj):
    return "A", obj[1:]


def inv_prod_fibo_2(obj):
    return "B", obj[1:]


def inv_prod_dyck_1(dyck):
    count = 1
    index = 1
    while (count != 0):
        if dyck[index] == "(":
            count += 1
        else:
            count -= 1
        index += 1
    return dyck[:index], dyck[index:]


def join_lambda(str1, str2):
    return str1 + str2


def len_div_2(string):
    if len(string) % 2 != 0:
        raise Exception
    return int(len(string) / 2)


def encaps(singleton, word):
    return singleton[0] + word + singleton[1]


def inv_encaps_dyck(dyck):
    return "()", dyck[1:-1]


def split_first(string):
    return string[0], string[1:]


def inv_union_vide_nonvide(string):
    return 0 if string == "" else 1


def inv_union_first_a(string):
    return 0 if (len(string) > 0 and string[0] == "A") else 1


def inv_union_first_b(string):
    return 0 if (len(string) > 0 and string[0] == "B") else 1


def inv_union_first_aa(string):
    return 0 if (len(string) > 1 and string[0] == "A" and string[1] == "A") else 1


def inv_union_first_bb(string):
    return 0 if (len(string) > 1 and string[0] == "B" and string[1] == "B") else 1


def inv_encaps_palin(palin):
    return palin[0] + palin[-1], palin[1:-1]


def inv_union_sing_nonsing(string):
    return 0 if (len(string) == 1) else 1


def inv_prod_sameAB_need_a(string):
    count_b_minus_a = 0
    i = 0
    while(count_b_minus_a != -1):
        if (string[i] == "A"):
            count_b_minus_a -= 1
        else:
            count_b_minus_a += 1
        i += 1
    return string[:i], string[i:]

def inv_prod_sameAB_need_b(string):
    count_b_minus_a = 0
    i = 0
    while(count_b_minus_a != 1):
        if (string[i] == "A"):
            count_b_minus_a -= 1
        else:
            count_b_minus_a += 1
        i += 1
    return string[:i], string[i:]

the_grammars = {
    "treeGram":{
            "Tree": UnionRule("Node", "Leaf", invert_union_tree, size),
            "Node": ProductRule("Tree", "Tree", lambda a, b: Node(a, b), invert_node, size),
            "Leaf": SingletonRule(Leaf)},
    "fiboGram":{
            "Fib": UnionRule("Vide", "Cas1", inv_union_fibo_1, size_fibo),
            "Cas1": UnionRule("CasAu", "Cas2", inv_union_fibo_2, size_fibo),
            "Cas2": UnionRule("AtomB", "CasBAu", inv_union_fibo_3, size_fibo),
            "CasAu": ProductRule("AtomA", "Fib", join_lambda, inv_prod_fibo_1, size_fibo),
            "CasBAu": ProductRule("AtomB", "CasAu", join_lambda, inv_prod_fibo_2, size_fibo),
            "Vide": EpsilonRule(""),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B")},
    "ABAlphabetGram":{
            "Mot": UnionRule("Vide", "NonVide", inv_union_vide_nonvide, len),
            "NonVide": ProductRule("Singleton", "Mot", join_lambda, split_first, len),
            "Singleton": UnionRule("AtomA", "AtomB", inv_union_first_a, len),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B"),
            "Vide": EpsilonRule("")},
    "dyckGram":{
            "Dyck": UnionRule("Vide", "NonVide", inv_union_vide_nonvide, len_div_2),
            "NonVide": ProductRule("DyckPremier", "Dyck", join_lambda, inv_prod_dyck_1, len_div_2),
            "DyckPremier": ProductRule("Atom", "Dyck", encaps, inv_encaps_dyck, len_div_2),
            "Atom": SingletonRule("()"),
            "Vide": EpsilonRule("")},
    "not3Gram":{
            "Not3": UnionRule("Vide", "NonVide", inv_union_vide_nonvide, len),
            "NonVide": UnionRule("A_Max1A", "B_Max1B", inv_union_first_a, len),
            "A_Max1A": ProductRule("AtomA", "Max1A", join_lambda, split_first, len),
            "B_Max1B": ProductRule("AtomB", "Max1B", join_lambda, split_first, len),
            "Max1A": UnionRule("A_NoA", "NoA", inv_union_first_a, len),
            "Max1B": UnionRule("B_NoB", "NoB", inv_union_first_b, len),
            "A_NoA": ProductRule("AtomA", "NoA", join_lambda, split_first, len),
            "B_NoB": ProductRule("AtomB", "NoB", join_lambda, split_first, len),
            "NoB": UnionRule("Vide", "A_Max1A", inv_union_vide_nonvide, len),
            "NoA": UnionRule("Vide", "B_Max1B", inv_union_vide_nonvide, len),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B"),
            "Vide": EpsilonRule("")},
    "palinABGram":{
            "PalinAB": UnionRule("Vide", "NonVide", inv_union_vide_nonvide, len),
            "NonVide": UnionRule("Singleton", "NonSingleton", inv_union_sing_nonsing, len),
            "NonSingleton": ProductRule("Doublet", "PalinAB", encaps, inv_encaps_palin, len),
            "Doublet": UnionRule("DoubletA", "DoubletB", inv_union_first_aa, len),
            "DoubletA": ProductRule("AtomA", "AtomA", join_lambda, split_first, len),
            "DoubletB": ProductRule("AtomB", "AtomB", join_lambda, split_first, len),
            "Singleton": UnionRule("AtomA", "AtomB", inv_union_first_a, len),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B"),
            "Vide": EpsilonRule("")},
    "palinABCGram":{
            "PalinABC": UnionRule("Vide", "NonVide", inv_union_vide_nonvide, len),
            "NonVide": UnionRule("Singleton", "NonSingleton", inv_union_sing_nonsing, len),
            "NonSingleton": ProductRule("Doublet", "PalinABC", encaps, inv_encaps_palin, len),
            "Doublet": UnionRule("DoubletA", "DoubletBouC", inv_union_first_aa, len),
            "DoubletBouC": UnionRule("DoubletB", "DoubletC", inv_union_first_bb, len),
            "DoubletA": ProductRule("AtomA", "AtomA", join_lambda, split_first, len),
            "DoubletB": ProductRule("AtomB", "AtomB", join_lambda, split_first, len),
            "DoubletC": ProductRule("AtomC", "AtomC", join_lambda, split_first, len),
            "Singleton": UnionRule("AtomA", "AtomBouC", inv_union_first_a, len),
            "AtomBouC": UnionRule("AtomB", "AtomC", inv_union_first_b, len),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B"),
            "AtomC": SingletonRule("C"),
            "Vide": EpsilonRule("")},
    "sameABGram":{
            "SameAB": UnionRule("Vide", "NonVide", inv_union_vide_nonvide, len),
            "NonVide": UnionRule("A_needBu", "B_needAu", inv_union_first_a, len),
            "A_needBu": ProductRule("AtomA", "NeedBu", join_lambda, split_first, len),
            "B_needAu": ProductRule("AtomB", "NeedAu", join_lambda, split_first, len),
            "NeedAu": ProductRule("NeedA", "SameAB", join_lambda, inv_prod_sameAB_need_a, len),
            "NeedBu": ProductRule("NeedB", "SameAB", join_lambda, inv_prod_sameAB_need_b, len),
            "NeedA": UnionRule("AtomA", "B_Need2A", inv_union_first_a, len),
            "NeedB": UnionRule("AtomB", "A_Need2B", inv_union_first_b, len),
            "A_Need2B": ProductRule("AtomA", "Need2B", join_lambda, split_first, len),
            "B_Need2A": ProductRule("AtomB", "Need2A", join_lambda, split_first, len),
            "Need2A": ProductRule("NeedA", "NeedA", join_lambda, inv_prod_sameAB_need_a, len),
            "Need2B": ProductRule("NeedB", "NeedB", join_lambda, inv_prod_sameAB_need_b, len),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B"),
            "Vide": EpsilonRule("")},
    "condensedGram":{"Tree" : Union(Singleton(Leaf), Prod(NonTerm("Tree"), NonTerm("Tree"), lambda a, b: Node(a, b)))}}