from grammar.Grammar import Grammar

grammar = Grammar('S',
                  ['S', 'A', 'C', 'D'],
                  ['a', 'b'],
                  {
                    'S': ["aA"],
                    'A': ["bS", "bD"],
                    'C': ["a", "bA"],
                    'D': ["bC", "aD"]
                  },
                  {'a'})

for i in range(5):
        string = grammar.printString()
        print(string)

fa = grammar.toFA()

input_string1 = 'ababb'
print('The input string is ' + input_string1 + '. Is it accepted?')
print(fa.accept(input_string1))  # Output: False

input_string2 = 'abababbbbaaabbbabbbabababababa'
print('The input string is ' + input_string2 + '. Is it accepted?')
print(fa.accept(input_string2))  # Output: True