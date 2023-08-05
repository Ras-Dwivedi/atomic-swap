class KripkeStructure:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.labels = {}

    def add_state(self, state, label):
        self.states.add(state)
        self.labels[state] = label
        if state not in self.transitions:
            self.transitions[state] = set()

    def add_transition(self, from_state, to_state):
        if from_state in self.states and to_state in self.states:
            self.transitions[from_state].add(to_state)
        else:
            raise ValueError("Invalid state in transition.")

    def get_successors(self, state):
        return self.transitions.get(state, set())

    def get_label(self, state):
        return self.labels.get(state, None)

    def __str__(self):
        return f"States: {self.states}\nTransitions: {self.transitions}\nLabels: {self.labels}"