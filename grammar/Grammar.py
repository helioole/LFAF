from finiteautomata.FiniteAutomata import FiniteAutomaton
import random

class Grammar:
    def __init__(self, startSymbol, nonTerminal, terminals,
                 productions, final):
        self.startSymbol = startSymbol
        self.terminals = terminals
        self.nonTerminal = nonTerminal
        self.productions = productions
        self.final = final

    def generateString(self, symbol: str) -> str:
        string = ''
        if symbol not in self.terminals:
            index = self.productions[symbol]
            chooseVn = random.choice(index)
            for i in chooseVn:
                string += self.generateString(i)
            return string
        else:
            return symbol

    def printString(self) -> str:
        return self.generateString(self.startSymbol)

    def toFA(self):
        alphabet = set(self.terminals)
        states = self.nonTerminal
        transitions = self.PtoT()
        start_state = 'S'
        final_state = {'a'}
        finite_automaton = FiniteAutomaton(alphabet, states, start_state, transitions, final_state)
        return finite_automaton

    def PtoT(self):
        transition = {}

        for non_terminal, productions in self.productions.items():
            transitions = {}
            for production in productions:
                if len(production) == 1:
                    transitions[production] = 'a'
                elif production[0] not in transitions:
                    transitions[production[0]] = [production[1]]
                else:
                    transitions[production[0]].append(production[1])
            transition[non_terminal] = transitions

        return transition