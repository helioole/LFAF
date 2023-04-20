from converter.ChomskyNormalForm import Chomsky

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

    print("Original Context Free Grammar:")
    chomsky.print_grammar()
    print("\n")

    print("After eliminating epsilon productions:")
    chomsky.eliminate_epsilon_productions()
    chomsky.print_grammar()
    print("\n")

    print("After eliminating unit productions:")
    chomsky.eliminate_unit_productions()
    chomsky.print_grammar()
    print("\n")

    print("After eliminating inaccessible symbols:")
    chomsky.eliminate_inaccessible_symbols()
    chomsky.print_grammar()
    print("\n")

    print("After eliminating non-productive productions:")
    chomsky.eliminate_nonproductive()
    chomsky.print_grammar()
    print("\n")

    print("Chomsky Normal Form:")
    chomsky.cfg_to_cnf()
    chomsky.print_grammar()

main()