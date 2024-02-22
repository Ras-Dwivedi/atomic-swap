"""
This class models the generic Kripke structure with all the states and the transition relations

@author: Ras Dwivedi
date : 04/08/2023

"""
from typing import Set, Any


class PathNotFoundError(Exception):
    pass

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

    def get_predecessor(self, state):
        predecessor_states = set()

        for from_state, successors in self.transitions.items():
            if state in successors:
                predecessor_states.add(from_state)

        return predecessor_states

    def find_transition_path(self, from_state, to_state):
        def dfs(state, visited_states, path):
            if state in visited_states:
                return False

            visited_states.add(state)
            path.append(state)

            if state == to_state:
                return True

            for successor in self.get_successors(state):
                if dfs(successor, visited_states, path):
                    return True

            path.pop()
            return False

        visited_states = set()
        path = []
        if dfs(from_state, visited_states, path):
            return path
        else:
            raise PathNotFoundError("Path not found from the first state to the second state.")

    def count_states(self, label):
        """
        counts the number of the states with the label in the KripkeStructure

        @returns 
            - number of the state with the given label
        """

        count = 0
        for state in self.states:
            if self.get_label(state) == label:
                count = count+1
        return count

    def get_states_with_label(self, target_label):
        states_with_label = []

        for state in self.states:
            label = self.get_label(state)
            if label == target_label:
                states_with_label.append(state)

        return states_with_label

    def find_reachable_states(self, state) -> Set[Any]:
        """
        Returns the set of reachable states of the given state
        """
        # Initialize a stack for DFS and a set to store visited states
        stack = []
        visited = set()

        stack.append(state)
        visited.add(state)

        # Perform DFS to find reachable states
        while stack:
            current_state = stack.pop()
            successors = self.get_successors(current_state)
            for successor in successors:
                if successor not in visited:
                    visited.add(successor)
                    stack.append(successor)

        return visited
