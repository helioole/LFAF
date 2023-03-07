import graphviz

from grammar.Grammar import Grammar
from finiteautomata.FiniteAutomata import FiniteAutomaton

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

fa1 = FiniteAutomaton(['q0', 'q1', 'q2'],
                          ['a', 'b'],
                          'q0',
                          [
                              ('q0', 'b', 'q0'),
                              ('q0', 'b', 'q1'),
                              ('q1', 'b', 'q2'),
                              ('q0', 'a', 'q0'),
                              ('q2', 'a', 'q2'),
                              ('q1', 'a', 'q1')
                          ],
                          {'q2'})
#Lab1
# for i in range(5):
#         string = grammar.printString()
#         print(string)
# fa = grammar.toFA()
# input_string1 = 'ababb'
# print('The input string is ' + input_string1 + '. Is it accepted?')
# print(fa.accept(input_string1))  # Output: False
#
# input_string2 = 'abababbbbaaabbbabbbabababababa'
# print('The input string is ' + input_string2 + '. Is it accepted?')
# print(fa.accept(input_string2))  # Output: True


#Lab2
# dot = graphviz.Digraph('NFA', filename='reports/lab2/nfa.gv')
# for state in fa1.states:
#     dot.node(str(state))
#
# dot.attr('node', shape='none')
# dot.edge('', str(fa1.start_state), arrowhead='normal')
#
# dot.attr('node', shape='doublecircle')
# for final in fa1.final_states:
#     dot.node(str(final), shape='doublecircle')
#
# dot.attr('node', shape='circle')
# dot.attr('edge', arrowhead='normal')
# for (state, symbol, next_state) in fa1.transitions:
#     dot.edge(state, next_state, label=symbol)
# dot.view()


CheckGrammar = grammar.Chomsky()
print(CheckGrammar)
print("\n")

grammar1 = fa1.convert()
print("Start symbol: ", grammar1.startSymbol)
print("Non-terminal symbols: ", grammar1.nonTerminal)
print("Terminal symbols: ", grammar1.terminals)
print("Productions: ", grammar1.productions)

print("\n")
if fa1.is_deterministic():
    print("The given finite automata is Deterministic")
else:
    print("The given finite automata is Non-deterministic")

print("\n")
dfa = fa1.NFAtoDFA()

print("After converting NFA to DFA:")

if dfa.is_deterministic():
    print("The given finite automata is Deterministic")
else:
    print("The given finite automata is Non-deterministic")


# dot = graphviz.Digraph('DFA', filename='reports/lab2/dfa.gv')
# for state in dfa.states:
#     dot.node(str(state))
#
# dot.attr('node', shape='none')
# dot.edge('', str(dfa.start_state), arrowhead='normal')
#
# dot.attr('node', shape='doublecircle')
# for final in dfa.final_states:
#     dot.node(str(final), shape='doublecircle')
#
# dot.attr('node', shape='circle')
# dot.attr('edge', arrowhead='normal')
# for (state, symbol, next_state) in dfa.transitions:
#     dot.edge(str(state), str(next_state), label=symbol)
# dot.view()