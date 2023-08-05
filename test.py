from collections import deque
from KripkeStructure import KripkeStructure

def find_reachable_states(kripke, start_states):
    # Initialize a queue for BFS and a set to store visited states
    queue = deque(start_states)
    visited = set(start_states)

    # Perform BFS to find reachable states
    while queue:
        current_state = queue.popleft()
        successors = kripke.get_successors(current_state)
        for successor in successors:
            if successor not in visited:
                visited.add(successor)
                queue.append(successor)

    return visited

# Example usage:
if __name__ == "__main__":
    # Create a Kripke structure
    kripke = KripkeStructure()

    # Adding states with labels
    kripke.add_state("s1", "good")
    kripke.add_state("s2", "good")
    kripke.add_state("s3", "bad")

    # Adding transitions
    kripke.add_transition("s1", "s2")
    kripke.add_transition("s2", "s3")
    kripke.add_transition("s3", "s1")
    kripke.add_transition("s3", "s2")

    # Define the start states
    start_states = ["s1", "s2"]

    # Find reachable states from the start states
    reachable_states = find_reachable_states(kripke, start_states)

    print("Reachable States from the start states:")
    print(reachable_states)
