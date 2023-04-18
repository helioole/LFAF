from grammar.ChomskyNormalForm import Chomsky

def main():
    chomsky = Chomsky('S',
    ['S', 'A', 'B', 'C'],
    ['a', 'd'],
    {
    'S': ["dB", "A"],
    'A': ["d", "dS", "aBdAB"],
    'B': ["a", "dA", "A", "ε"],
    'C': ["Aa"]
    })

    # chomsky = Chomsky('S',
    #                   ['S', 'A', 'B', 'C', 'D'],
    #                   ['a', 'b'],
    #                   {
    #                       'S': ["a", "aD", "aA", "B"],
    #                       'A': ["aBB", "ε"],
    #                       'D': ["aD"],
    #                       'C': ["aC"],
    #                       'B': ["Aa", "b"]
    #                   })

    chomsky1 = Chomsky('S',
    ['S', 'A', 'B', 'C', 'E'],
    ['a', 'b'],
    {
    'S': ["aB", "AC"],
    'A': ["a", "ASC", "BC"],
    'B': ["b", "bS"],
    'C': ["ε", "BA"],
    'E': ["bB"]
    })

    chomsky2 = Chomsky('S',
    ['S', 'A', 'B', 'C', 'D'],
    ['a', 'd'],
    {
    'S': ["bA", "AC"],
    'A': ["bS", "BC", "AbAa"],
    'B': ["BbaA", "a", "bSa"],
    'C': ["ε"],
    'D': ["AB"]
    })

    # chomsky.eliminate_epsilon_productions()
    # print(chomsky.productions)
    # print(chomsky.nonTerminal)

    # print(chomsky.productions)
    # print(chomsky.nonTerminal)
    #
    chomsky.eliminate_epsilon_productions()
    print(chomsky.productions)
    print(chomsky.nonTerminal)
    chomsky.eliminate_unit_productions()
    print(chomsky.productions)
    print(chomsky.nonTerminal)
    chomsky.eliminate_inaccessible_symbols()
    print(chomsky.productions)
    print(chomsky.nonTerminal)
    chomsky.eliminate_nonproductive()
    print(chomsky.productions)
    print(chomsky.nonTerminal)



    # chomsky.cfg_to_cnf()
    # chomsky.print_grammar()

main()