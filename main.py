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

main()