import random
import functools32
from copy import deepcopy

class AbstractRule(object):
    """
    This class will represent every rule used in the project (Constructor and Constant)
    """
    def _set_grammar(self, gram):
        self._grammar = gram
        
    def random(self, n):
        return self.unrank(n, random.randint(0, self.count(n) - 1))
        
class ConstructorRule(AbstractRule):
    """
    This class descends from AbstractRule as indicated in the description,
    """
    def __init__(self, fst, snd, size):
        """
        Input:
        - fst and snd represent both a non-terminal rule of the grammar
        - size represents the function that can find the size of an object
        """
        self._parameters = (fst, snd)
        self._valuation = float("inf")
        self._size = size
    
    def valuation(self):
        return self._valuation
        
    def _update_valuation(self):
        self._valuation = self._calc_valuation()
        
class UnionRule(ConstructorRule):
    
    def __init__(self, fst, snd, invert_union = None, size = None):
        """
        Input:
        - fst and snd represent both a non-terminal rule of the grammar
        - size represents the function that can find the size of an object
        - invert_union represents a function that receives the result of 
        the union rule over two objects and is able to retreive both original values
        """
        ConstructorRule.__init__(self, fst, snd, size)
        self._invert_union = invert_union
        
    def _calc_valuation(self):
        """
        finds the size of the smallest derived object
        """
        return min([self._grammar[parameter].valuation() for parameter in self._parameters])
    
    @functools32.lru_cache(maxsize=100)
    def count(self, n):
        """
        This function returns the number of objects of type n
        Input:
        - n represents the size of the objects
        """
        return sum([self._grammar[parameter].count(n) for parameter in self._parameters])
    
    @functools32.lru_cache(maxsize=100)
    def list(self, n):
        """
        This functions returns a list with all elements of size n
        Input:
        - n represents the size of the objects
        """
        answer = []
        for parameter in self._parameters:
            answer += self._grammar[parameter].list(n)
        return answer
    
    @functools32.lru_cache(maxsize=100)
    def unrank(self, n, i):
        """
        This function finds the element of rank "rank" and returns it
        Input:
        - n is the size of the desired object
        - rank is its desired rank
        """
        if i >= self.count(n):
            raise ValueError
        else:
            C_a = self._grammar[self._parameters[0]].count(n)
            if i < C_a:
                return self._grammar[self._parameters[0]].unrank(n, i)
            else:
                return self._grammar[self._parameters[1]].unrank(n, i - C_a)

    @functools32.lru_cache(maxsize=100)
    def rank(self, obj):
        """
        This function finds the rank of the element obj
        Input:
        - obj is the object to be ranked
        """
        if self._invert_union is None or self._size is None:
            raise ValueError("Inversion functions have to be provided for rank usage")
        if self._invert_union(obj) == 0:
            return self._grammar[self._parameters[0]].rank(obj)
        else:
            return self._grammar[self._parameters[0]].count(self._size(obj)) + self._grammar[self._parameters[1]].rank(obj)
    
class ProductRule(ConstructorRule):
    
    def __init__(self, fst, snd, cons, invert_prod = None, size = None):
        """
        Input:
        - fst and snd represent both a non-terminal rule of the grammar
        - size represents the function that can find the size of an object
        - cons represents the function that will be applied to both fst and snd
        - invert_prod represents a function that receives the result of 
        the product rule over two objects and is able to retreive both original values
        """
        ConstructorRule.__init__(self, fst, snd, size)
        self._constructor = cons
        self._invert_constructor = invert_prod
        
    def _calc_valuation(self):
        """
        finds the size of the smallest derived object
        """
        return sum([self._grammar[parameter].valuation() for parameter in self._parameters])
    
    @functools32.lru_cache(maxsize=100)
    def count(self, n):
        """
        This function returns the number of objects of type n
        Input:
        - n represents the size of the objects
        """
        total_sum = 0
        vals = [self._grammar[parameter].valuation() for parameter in self._parameters]
        for k in range(vals[0], n+1):
            l = n - k
            if l >= vals[1]:
                aux = [self._grammar[self._parameters[0]].count(k), self._grammar[self._parameters[1]].count(l)]
                total_sum += aux[0]*aux[1]
        return total_sum
    
    @functools32.lru_cache(maxsize=100)
    def list(self, n):
        """
        This functions returns a list with all elements of size n
        Input:
        - n represents the size of the objects
        """
        answer = []
        vals = [self._grammar[parameter].valuation() for parameter in self._parameters]
        for k in range(vals[0], n+1):
            l = n - k
            if l >= vals[1]:
                auxans = (self._grammar[self._parameters[0]].list(k), self._grammar[self._parameters[1]].list(l))
                for elem0 in auxans[0]:
                    for elem1 in auxans[1]:
                        answer.append(self._constructor(elem0, elem1))
        return answer

    @functools32.lru_cache(maxsize=100)
    def unrank(self, n, rank):
        """
        This function finds the element of rank "rank" and returns it
        Input:
        - n is the size of the desired object
        - rank is its desired rank
        """
        if rank >= self.count(n):
            raise ValueError
        else:
            first_nonterm = self._grammar[self._parameters[0]]
            second_nonterm = self._grammar[self._parameters[1]]
            count = 0
            last_count = 0
            index = 0
            while count <= rank and index <= n:
                last_count = count
                count += first_nonterm.count(index) * second_nonterm.count(n - index)
                index += 1
            if count <= rank:
                raise ValueError
            index -= 1
            difference = rank - last_count
            k = second_nonterm.count(n - index)
            quotient, rest = difference/k, difference % k
            return self._constructor(first_nonterm.unrank(index, quotient), second_nonterm.unrank(n-index, rest))
    
    @functools32.lru_cache(maxsize=100)
    def rank(self, obj):
        """
        This function finds the rank of the element obj
        Input:
        - obj is the object to be ranked
        """
        if self._invert_constructor is None or self._size is None:
            raise ValueError("Inversion functions have to be provided for rank usage")
        first_nonterm = self._grammar[self._parameters[0]]
        second_nonterm = self._grammar[self._parameters[1]]
        obj_fst, obj_snd = self._invert_constructor(obj)
        n = self._size(obj)
        n_left = self._size(obj_fst)
        r_fst = first_nonterm.rank(obj_fst)
        r_snd = second_nonterm.rank(obj_snd)
        count = sum(first_nonterm.count(i) * second_nonterm.count(n - i) for i in range(n_left))
        return count + r_fst * second_nonterm.count(n - n_left) + r_snd
                    
class ConstantRule(AbstractRule):
    
    def __init__(self, object):
        self._object = object
        
class SingletonRule(ConstantRule):
    
    def __init__(self, obj):
        ConstantRule.__init__(self, obj)
        
    def valuation(self):
        """
        finds the size of the smallest derived object
        """
        return 1
    
    def count(self, n):
        """
        This function returns the number of objects of type n
        Input:
        - n represents the size of the objects
        """
        if n == 1:
            return 1
        else:
            return 0
        
    def list(self, n):
        """
        This functions returns a list with all elements of size n
        Input:
        - n represents the size of the objects
        """
        if n == 1:
            return [self._object]
        else:
            return []
        
    def unrank(self, n, rank):
        """
        This function finds the element of rank "rank" and returns it
        Input:
        - n is the size of the desired object
        - rank is its desired rank
        """
        if rank >= self.count(n):
            raise ValueError
        else:
            return self._object

    def rank(self, obj):
        """
        This function finds the rank of the element obj
        Input:
        - obj is the object to be ranked
        """
        if obj == self._object:
            return 0
        else:
            raise "Not a correct object"
    
class EpsilonRule(ConstantRule):
    
    def __init__(self, obj):
        ConstantRule.__init__(self, obj)
        
    def valuation(self):
        """
        finds the size of the smallest derived object
        """
        return 0
    
    def count(self, n):
        """
        This function returns the number of objects of type n
        Input:
        - n represents the size of the objects
        """
        if n == 0:
            return 1
        else:
            return 0
        
    def list(self, n):
        """
        This functions returns a list with all elements of size n
        Input:
        - n represents the size of the objects
        """
        if n == 0:
            return [self._object]
        else:
            return []
        
    def unrank(self, n, rank):
        """
        This function finds the element of rank "rank" and returns it
        Input:
        - n is the size of the desired object
        - rank is its desired rank
        """
        if rank >= self.count(n):
            raise ValueError
        else:
            return self._object

    def rank(self, obj):
        """
        This function finds the rank of the element obj
        Input:
        - obj is the object to be ranked
        """
        if obj == self._object:
            return 0
        else:
            raise "Not a correct object"

class Union:
    def __init__(self, fst, snd):
        self._fst = fst
        self._snd = snd

    def convert(self, gram, new_key=None):
        key_fst = self._fst.convert(gram)
        key_snd = self._snd.convert(gram)
        new_key = new_key or "U("+str(key_fst)+", "+str(key_snd)+")"
        gram[new_key] = UnionRule(key_fst, key_snd)
        return new_key


class Prod:
    def __init__(self, fst, snd, cons):
        self._fst = fst
        self._snd = snd
        self._constructor = cons

    def convert(self, gram, new_key=None):
        key_fst = self._fst.convert(gram)
        key_snd = self._snd.convert(gram)
        new_key = new_key or "P("+str(key_fst)+", "+str(key_snd)+")"
        gram[new_key] = ProductRule(key_fst, key_snd, self._constructor)
        return new_key


class Singleton:
    def __init__(self, obj):
        self._obj = obj

    def convert(self, gram, new_key=None):
        new_key = new_key or "S-"+str(self._obj)
        gram[new_key] = SingletonRule(self._obj)
        return new_key


class Epsilon:
    def __init__(self, obj):
        self._obj = obj

    def convert(self, gram, new_key=None):
        new_key = new_key or "E-"+str(self._obj)
        gram[new_key] = EpsilonRule(self._obj)
        return new_key

class NonTerm:
    def __init__(self, string):
        self._str = string

    def convert(self, gram, new_key=None):
        if gram[self._str] is None:
            raise Exception("NonTerm is not in the grammar")
        return self._str

class Bound:
    def __init__(self, C, the_min, the_max):
        self._class = C
        self._min = the_min
        self._max = the_max

    def list(self):
        if self._min > self._max:
            raise "Max should be larger than Min"
        else:
            return [C.count(i) for i in range(self._min, self._max+1)]
        
def init_grammar(grammar):
    """
    This function initiates the grammar "grammar"
    Input:
    - "grammar" is a grammar
    - is_condensed is boolean that is true iff the grammar is condensed
    """
    for rule_key in grammar:
        if hasattr(grammar[rule_key], "_set_grammar"):
            grammar[rule_key]._set_grammar(grammar)
    valuations = [float("inf")]*len(grammar)
    newvaluations = [grammar[key].valuation() for key in grammar]
    while newvaluations != valuations:
        valuations = newvaluations
        for rule_key in grammar:
            if isinstance(grammar[rule_key], ConstructorRule):
                grammar[rule_key]._update_valuation()
        newvaluations = [grammar[key].valuation() for key in grammar]
    return

class Bound:
    def __init__(self, C, the_min, the_max):
        """
        This will give a constructor that iterates over the lists of objects
        with sizes between the_min and the_max
        Input:
        - C represents a class of objects
        - the_min and the_max are integers representing the minimum and maximum sizes of the wanted objects
        """
        self.C = C
        self.min = the_min
        self.max = the_max

    def __iter__(self):
        """
        Iterates over the lists of objects C
        """
        for list_i in range(self.min, self.max+1):
            for value_i in range(self.C.count(list_i)):
                yield self.C.list(list_i)[value_i]

def convert_condensed_gram(cond_grammar):
    """
    This functions converts a condensed grammar into a normal gramma
    Input:
    - cond_grammar is a condensed_grammar
    """
    new_grammmar = deepcopy(cond_grammar)
    cond_grammar[cond_grammar.keys()[0]].convert(new_grammmar, cond_grammar.keys()[0])
    return new_grammmar