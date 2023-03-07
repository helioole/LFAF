# from finiteautomata.FiniteAutomata import FiniteAutomaton
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

    # def toFA(self):
    #     alphabet = set(self.terminals)
    #     states = self.nonTerminal
    #     transitions = self.PtoT()
    #     start_state = 'S'
    #     final_state = {'F'}
    #     finite_automaton = FiniteAutomaton(alphabet, states, start_state, transitions, final_state)
    #     return finite_automaton

    def PtoT(self):
        transition = {}

        for non_terminal, productions in self.productions.items():
            transitions = {}
            for production in productions:
                if len(production) == 1:
                    transitions[production] = 'F'
                elif production[0] not in transitions:
                    transitions[production[0]] = [production[1]]
                else:
                    transitions[production[0]].append(production[1])
            transition[non_terminal] = transitions

        return transition

    def Chomsky(self):
        type1 = True
        type2 = True
        type3_right = True
        type3_left = True

        for non_terminal in self.nonTerminal:
            for production in self.productions[non_terminal]:
                if (len(production) == 2 and production[1] not in self.nonTerminal and
                    production[0] not in self.terminals) \
                        or len(production) > 2:
                    type3_right = False
                    break

                if (len(production) == 1 and production[0] not in self.terminals) \
                        or (len(production) == 2 and production[0] not in self.nonTerminal) \
                        or len(production) > 2:
                    type3_left = False
                    break

                if any(len(lst) > 2 for lst in production) or any(len(lst) == 0 for lst in production):
                    type2 = False
                    break

                if len(production) == 0:
                    type1 = False
                    break

        for production in self.productions.keys():
            if len(production) != 1:
                type2 = False
                break

            if all(len(p) < 1 for p in production):
                type1 = False
                break

        if type3_right:
            return 'Type 3 Right linear grammar'
        elif type3_left:
            return 'Type 3 Left linear grammar'
        elif type2:
            return 'Type 2'
        elif type1:
            return 'Type 1'
        else:
            return 'Type 0'
