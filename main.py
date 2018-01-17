from all_grammars import the_grammars
from Rules import init_grammar, convert_condensed_gram
from Node import Node, Leaf

treeGram = the_grammars["treeGram"]
init_grammar(treeGram)

for rule in treeGram:
	print rule, treeGram[rule].valuation()