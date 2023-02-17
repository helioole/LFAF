class FiniteAutomaton:
    def __init__(self, alphabet, states, start_state, transitions, final_states):
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