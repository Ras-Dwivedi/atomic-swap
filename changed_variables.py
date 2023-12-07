def get_changed_variables(from_state, to_state):
    """
    returns the changes variables as the dictionary containing the from and the to state
    """
    changed_variables = {}

    # Check for changes in each component of the states
    for i, (from_value, to_value) in enumerate(zip(from_state, to_state)):
        if from_value != to_value:
            variable_name = ['a', 'b', 'x1', 'x2', 'y1', 'y2', 's1', 's2'][i]
            changed_variables[variable_name] = (from_value, to_value)

    return changed_variables

# Example usage:
if __name__ == "__main__":
    from_state = (1, 0, 1, 0, 1, 0, 1, 1)
    to_state = (1, 1, 1, 0, 1, 0, 2, 1)

    changes = get_changed_variables(from_state, to_state)
    print(changes)
    print(len(changes))
    print("Changed variables:")
    for variable, (from_value, to_value) in changes.items():
        print(f"{variable}: {from_value} -> {to_value}")
