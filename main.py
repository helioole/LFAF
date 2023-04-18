from grammar.ChomskyNormalForm import Chomsky

chomsky = Chomsky('S',
['S', 'A', 'B', 'C'],
['a', 'd'],
{
'S': ["dB", "A"],
'A': ["d", "dS", "aBdAB"],
'B': ["a", "dA", "A", "ε"],
'C': ["Aa"]
})

chomsky.cfg_to_cnf()
chomsky.print_grammar()