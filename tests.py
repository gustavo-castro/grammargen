from all_grammars import the_grammars
from Rules import AbstractRule, ConstructorRule, UnionRule, ProductRule, ConstantRule, SingletonRule
from Rules import EpsilonRule, init_grammar, convert_condensed_gram, Bound
from Node import Node, Leaf

def is_grammar_correct(grammar):
    """
    This function checks if the grammar "grammar" is correct
    Input:
    - "grammar" is a grammar
    """
    allrules = set(grammar.keys())
    for rule_key in grammar:
        if isinstance(grammar[rule_key], ConstructorRule):
            for parameter in grammar[rule_key]._parameters:
                if parameter not in allrules:
                    return False
    return True

def check_list_and_count(grammar, to_size):
	"""
	This function will assert that a grammar list method gives a
	list whose length is the same as the value returned by the count method
	Input:
	- "grammar" is a grammar
	- to_size is an integer that represents the maximum size value we want to be testing
	"""
	for rule in grammar:
		for size in range(1,to_size):
			assert(len(grammar[rule].list(size)) == grammar[rule].count(size))
	return

def check_rank_and_unrank(grammar, to_size, is_condensed):
	"""
	This function will assert that a grammar list method gives a
	list whose length is the same as the value returned by the count method
	Input:
	- "grammar" is a grammar
	- to_size is an integer that represents the maximum size value we want to be testing
	"""
	for rule in grammar:
		for size in range(1,to_size):
			aux_list = grammar[rule].list(size)
			for index in range(grammar[rule].count(size)):
				if is_condensed:
					assert(grammar[rule].unrank(size, index) == aux_list[index])
				else:
					assert(grammar[rule].rank(grammar[rule].unrank(size, index)) == index)
	return

def check_bound(grammar, the_min, the_max):
	"""
	checks if the Bound constructor builds the correct elements
	Input:
	- "grammar" is a grammar
	- the_min and the_max are the range of values of sizes to be tested
	"""
	for rule in grammar:
		class_object = grammar[rule]
		flatten = lambda l: [item for sublist in l for item in sublist]
		aux_list = [class_object.list(i) for i in range(the_min, the_max+1)]
		aux_list = flatten(aux_list)
		assert(list(Bound(class_object, the_min, the_max)) == aux_list)

def check_all_grammars(the_grammars, max_size):
	"""
	Does all the tests described above with all the grammars in the all_grammars script
	Input:
	- the_grammars is a dictionary will all grammars
	- max_size is an integer representing the maximum size for the values on 
	"""
	for grammar in the_grammars:
		is_condensed = False
		if grammar == "condensedGram":
			the_grammars[grammar] = convert_condensed_gram(the_grammars[grammar])
			init_grammar(the_grammars[grammar])
			is_condensed = True
		else:
			init_grammar(the_grammars[grammar])			
		if is_grammar_correct(the_grammars[grammar]):
			check_list_and_count(the_grammars[grammar], max_size)
			check_rank_and_unrank(the_grammars[grammar], max_size, is_condensed)
			check_bound(the_grammars[grammar], 0, max_size)
		else:
			raise "Grammar is incorrect"

check_all_grammars(the_grammars, 10)

print "All tests in all grammars passed"