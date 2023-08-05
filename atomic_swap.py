from KripkeStructure import KripkeStructure

def add_states_to_kripke(kripke):
    total_states_inserted = 0

    for a in [0, 1]:
        for b in [0, 1]:
            for x1 in [0, 1]:
                for x2 in [0, 1]:
                    for y1 in [0, 1]:
                        for y2 in [0, 1]:
                            for s1 in range(4):
                                for s2 in range(4):
                                    state = (a, b, x1, x2, y1, y2, s1, s2)
                                    if s1==0:
                                        if s2==0:
                                            label = "good"
                                        if s2 == 3:
                                            label = "bad"
                                    elif s1==3:
                                        if s2 == 0:
                                            label = "bad"
                                        if s2 == 3:
                                            label = "good"
                                    else:
                                        label = 'unknown'
                                    kripke.add_state(state, label)
                                    total_states_inserted += 1

    return total_states_inserted

# Example usage:
if __name__ == "__main__":
    # Create a Kripke structure
    kripke = KripkeStructure()

    # Add states to the Kripke structure
    total_states = add_states_to_kripke(kripke)

    # Print the Kripke structure
    print(kripke)

    # Output the total number of states inserted
    print("Total states inserted:", total_states)
