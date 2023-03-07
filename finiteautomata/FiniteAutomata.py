from collections import defaultdict
from grammar.Grammar import Grammar

class FiniteAutomaton:
    def __init__(self, states, alphabet, start_state, transitions, final_states):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.transitions = transitions
        self.final_states = final_states

    def accept(self, input_string: str) -> bool:
        states = [self.start_state]
        for char in input_string:
            next_states = []
            for state in states:
                if state in self.transitions and char in self.transitions[state]:
                    next_states.extend(self.transitions[state][char])
            if not next_states:
                return False
            states = next_states
        return any(state in self.final_states for state in states)

    def is_deterministic(fa):
        transitions = defaultdict(set)

        for transition in fa.transitions:
            state, symbol, next_state = transition
            transitions[(state, symbol)].add(next_state)

        for (state, symbol) in transitions:
            if len(transitions[(state, symbol)]) > 1:
                return False
        return True

    def convert(self):
        non_terminals = self.states
        terminals = self.alphabet
        productions = {}
        start_symbol = self.start_state

        for s1, a, s2 in self.transitions:
            if s1 not in productions:
                productions[s1] = []
            productions[s1].append(a + s2)

        for state in self.final_states:
            if state not in productions:
                productions[state] = []

        return Grammar(start_symbol, non_terminals, terminals, productions, self.final_states)

    def NFAtoDFA(self):
        dfa_states = []
        dfa_transitions = []
        dfa_start_state = tuple([self.start_state])
        dfa_final_states = set()

        queue = [dfa_start_state]
        visited = {dfa_start_state}

        while queue:
            current_states = queue.pop(0)
            dfa_states.append(current_states)

            for symbol in self.alphabet:
                next_states = set()
                for state in current_states:
                    for transition in self.transitions:
                        if transition[0] == state and transition[1] == symbol:
                            next_states.add(transition[2])

                if not next_states:
                    continue

                next_states = tuple(sorted(next_states))

                if next_states not in visited:
                    visited.add(next_states)
                    queue.append(next_states)

                dfa_transitions.append((current_states, symbol, next_states))

                if any(state in next_states for state in self.final_states):
                    dfa_final_states.add(current_states)

        return FiniteAutomaton(dfa_states, self.alphabet, dfa_start_state, dfa_transitions, dfa_final_states)















