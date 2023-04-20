import unittest
from converter.ChomskyNormalForm import Chomsky



class TestConverter(unittest.TestCase):

    def test_remove_epsilon_productions(self):
        chomsky = Chomsky('S',
                          ['S', 'A', 'B', 'C'],
                          ['a', 'd'],
                          {
                              'S': ["dB", "A"],
                              'A': ["d", "dS", "aBdAB"],
                              'B': ["a", "dA", "A", "ε"],
                              'C': ["Aa"]
                          })

        chomsky.eliminate_epsilon_productions()
        new_productions = chomsky.productions
        new_nonTerminals = chomsky.nonTerminal
        expected_productions = {'S': ['d', 'dB', 'A'],
                                'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'B': ['a', 'dA', 'A'],
                                'C': ['Aa']}

        expected_terminals = ['S', 'A', 'B', 'C']

        self.assertCountEqual(new_productions, expected_productions)
        self.assertCountEqual(new_nonTerminals, expected_terminals)

    def test_remove_unit_productions(self):
        chomsky = Chomsky('S',
                          ['S', 'A', 'B', 'C'],
                          ['a', 'd'],
                          {'S': ['d', 'dB', 'A'],
                           'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                           'B': ['a', 'dA', 'A'],
                           'C': ['Aa']}
                          )

        chomsky.eliminate_unit_productions()
        new_productions = chomsky.productions
        new_nonTerminals = chomsky.nonTerminal
        expected_productions = {'S': ['d', 'dB', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'B': ['a', 'dA', 'd', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'C': ['Aa']}

        expected_terminals = ['S', 'A', 'B', 'C']

        self.assertCountEqual(new_productions, expected_productions)
        self.assertCountEqual(new_nonTerminals, expected_terminals)

    def test_inaccessible_symbols(self):
        chomsky = Chomsky('S',
                          ['S', 'A', 'B', 'C'],
                          ['a', 'd'],
                          {'S': ['d', 'dB', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                           'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                           'B': ['a', 'dA', 'd', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                           'C': ['Aa']}
                          )

        chomsky.eliminate_inaccessible_symbols()
        new_productions = chomsky.productions
        new_nonTerminals = chomsky.nonTerminal
        expected_productions = {'S': ['d', 'dB', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'B': ['a', 'dA', 'd', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA']}

        expected_terminals = ['S', 'A', 'B']

        self.assertCountEqual(new_productions, expected_productions)
        self.assertCountEqual(new_nonTerminals, expected_terminals)

    def test_remove_nonproductive_symbols(self):
        chomsky = Chomsky('S',
                          ['S', 'A', 'B', 'C'],
                          ['a', 'd'],
                          {'S': ['d', 'dB', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                           'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                           'B': ['a', 'dA', 'd', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA']}
                          )

        chomsky.eliminate_inaccessible_symbols()
        new_productions = chomsky.productions
        new_nonTerminals = chomsky.nonTerminal
        expected_productions = {'S': ['d', 'dB', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'A': ['d', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA'],
                                'B': ['a', 'dA', 'd', 'dS', 'adA', 'aBdAB', 'adAB', 'aBdA']}

        expected_terminals = ['A', 'B', 'S']

        self.assertCountEqual(new_productions, expected_productions)
        self.assertCountEqual(new_nonTerminals, expected_terminals)

if __name__ == '__unittest__':
    unittest.main()