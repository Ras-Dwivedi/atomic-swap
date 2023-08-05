from KripkeStructure import KripkeStructure
import time
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
                                    # elif s1 ==1 :
                                    #     if s2 == 3:
                                    #         label = "bad"
                                    # elif s1==3:
                                    #     if s2 == 0:
                                    #         label = "bad"
                                    #     if s2 == 3:
                                    #         label = "good"
                                    # elif s2==1:
                                    #     if s1 ==3:
                                    #         label = "bad"
                                    else:
                                        label = 'unknown'
                                    kripke.add_state(state, label)
                                    total_states_inserted += 1

    return total_states_inserted

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

def is_valid_transition(from_state, to_state):
    """
    the idea is that there are only certain set of the transition possible. 
    all other transition needs to be avoided. 
    default response is true. we are checking certain false transition
    """
    a, b, x1, x2, y1, y2, s1, s2 = from_state
    new_a, new_b, new_x1, new_x2, new_y1, new_y2, new_s1, new_s2 = to_state

    changes = get_changed_variables(from_state,to_state)
    keys = list(changes)

    #changes prohibited

    # known secrets cannote b forgetton
    # x1 cannot change from 1 to 0
    if x1 == 1 and new_x1 == 0:
        return False

    # y1 cannot change from 1 to 0
    if y1 == 1 and new_y1 == 0:
        return False

    # x2 cannot change from 1 to 0
    if x2 == 1 and new_x2 == 0:
        return False

    # y2 cannot change from 1 to 0
    if y2 == 1 and new_y2 == 0:
        return False

    # a cannot change from 1 to 0
    if a == 1 and new_a == 0:
        return False
    
    # b cannot change from 1 to 0
    if b == 1 and new_b == 0:
        return False
    
    #quit is only possible when the secret is revealed
    # if s1 goes from 1 to 0, then a must also become 1
    if s1 == 1 and new_s1 == 0 and new_a != 1:
        return False

    # if s2 goes from 1 to 0, then b must also become 1
    if s2 == 1 and new_s2 == 0 and new_b != 1:
        return False

    # freezing is only possible when the secret are known and revealed    
    # if s1 goes from 1 to 2, then x1, y1, y2 must also become 1
    if s1 == 1 and new_s1 == 2 and (new_x1, new_y1, new_y2) != (1, 1, 1):
        return False

    # if s2 goes from 1 to 2, then y1, x1, x2 must also become 1
    if s2 == 1 and new_s2 == 2 and (new_y1, new_x1, new_x2) != (1, 1, 1):
        return False


    # to abort, one must know the secret of the other party
    # if s1 goes from 2 to 0, then b must become 1
    if s1 == 2 and new_s1 == 0 and new_b != 1:
        return False

    # if s2 goes from 2 to 0, then a must become 1
    if s2 == 2 and new_s2 == 0 and new_a != 1:
        return False

    # to get the coin, all the secret must be revealed
    # if s1 goes from 2 to 3, then x1, x2, y1, y2 must also become 1
    if s1 == 2 and new_s1 == 3 and (x1, x2, y1, y2) != (1, 1, 1, 1):
        return False

    # if s2 goes from 2 to 3, then x1, x2, y1, y2 must also become 1
    if s2 == 2 and new_s2 == 3 and (x1, x2, y1, y2) != (1, 1, 1, 1):
        return False

    # from freeze on can only abort (return to 0) or resolve (move to 3)
    # not movement from 2 to 1
    if s1 == 2 and new_s1 == 1:
        return False

    if s2 == 2 and new_s2 == 1:
        return False

    # from 0 one can only move to 1

    if s1 == 0 and not (new_s1 == 1 or new_s1==0):
        return False

    if s2 == 0 and not (new_s2 == 1 or new_s2==0):
        return False

    # from 1 one cannot move to 3 directly
    if s1 == 1 and new_s1 == 3:
        return False

    if s2 == 1 and new_s2 == 3:
        return False
 

    # practical cases

    # a is revealed only when the contract is quit
    if (a==0 and new_a ==1):
        # print(from_state,to_state)
        # time.sleep(10)
        if not (s1 ==1 and new_s1 == 0):
            return False

    if (b==0 and new_b ==1):
        if not (s2 ==1 and new_s2 == 0):
            return False

    #if x2/y2 is revealed, either the x1/y1 is revealed in the same transaction, or the already revealed
    if x2==0 and new_x2 == 1:
        if not new_x1 ==1:
            return False

    if y2==0 and new_y2 == 1:
        if not new_y1 ==1:
            return False

    #why is this condition forced, and not implicit
    # x2/y2 is revealed only if y1/x1 has already been revealed
    # if x2/y2 is revealed, then the contract should be frozen
    if x2 == 0 and new_x2 ==1:
        if y1 ==0:
            return False
        if not (s2==1 and new_s2 ==2):
            return False 

    if y2 == 0 and new_y2 ==1:
        if x1 ==0:
            return False
        if not (s1==1 and new_s1 ==2):
            return False 

    return True



    # # No other kind of transitions allowed
    # if new_s1 not in {0, 1, 2, 3} or new_s2 not in {0, 1, 2, 3}:
    #     return False

def add_transition_to_kripke(kripke):
    count = 0
    for from_state in kripke.states:
        for to_state in kripke.states:
            # Apply the transition rules
            if is_valid_transition(from_state,to_state):

                # If all rules pass, add the transition
                kripke.transitions[from_state].add(to_state)
                count = count +1
    print(f"total transitions {count}")
    return count

def label_bad_states(kripke):
    """
    labels all the bad state in the kripke structure
    """
    for state in kripke.states:
        label_bad_state(kripke, state)
    no_bad_states = count_bad_states(kripke)
    # print(kripke)
    print(f"numbers of the bad states as {no_bad_states}")
    print(f"total number of the states are {total_states}")

def label_bad_state(kripke, unknown_state):
    """
    marks the state as the bad state if any of the future state reached by it is bad state
    """
    def dfs(state, visited_states):
        """
        returns True if any of the successor state is a bad state
        else returns false
        """
        if state in visited_states:
            return

        visited_states.add(state)

        #if the state itself is bad return True
        if kripke.get_label(state) == "bad":
            # print(f'reached state {state}, which is bad')
            return True

        #if the any of the sucessor is bad, label it bad
        for successor in kripke.get_successors(state):
            if dfs(successor, visited_states):
                return True

        return False

    visited_states = set()
    if dfs(unknown_state, visited_states):
        kripke.labels[unknown_state] = "bad"
        # try:
        #     path = find_transition_path(unknown_state,(1,1,1,1,1,1,3,0))
        #     print(path)
        # except Exception as e:
        #     print("no path found")
        # print(f"state {unknown_state} labelled as bad")


def count_bad_states(kripke):
    """
    counts the number of the bad states in the kripke KripkeStructure
    @param
        -kripke structure
    @returns 
        - number of the bad states
    """

    count = 0
    for state in kripke.states:
        if kripke.get_label(state) == "bad":
            count = count+1
    return count


class PathNotFoundError(Exception):
    pass

def find_transition_path(kripke, from_state, to_state):
    def dfs(state, visited_states, path):
        if state in visited_states:
            return False

        visited_states.add(state)
        path.append(state)

        if state == to_state:
            return True

        for successor in kripke.get_successors(state):
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

# Example usage:

def print_state(state):
    names = ['a', 'b', 'x1', 'x2', 'y1', 'y2', 's1', 's2']
    # state = enumerate(_state)
    for i in range(len(names)):
        print(f' {names[i]}={state[i] }', end="")
    print("\n")




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
    total_transition = add_transition_to_kripke(kripke)
    print("total transitions inserted", total_transition)
    print("labelling the bad states")
    label_bad_states(kripke)
    
    # label_bad_state(kripke,(0,0,0,0,0,0,0,0))
    # print(kripke.get_label((0,0,0,0,0,0,0,0)))
    # # print(kripke.get_successors((0,0,0,0,0,0,0,0)))

    try:
        s1 = (0,0,0,0,0,0,0,0)
        # s2 = (0,0,0,0,0,0,0,3)
        s2 =  (1, 1, 1, 1, 1, 1, 0, 3)
        path = find_transition_path(kripke, s1, s2)
        for state in path:
            print_state(state)
        # print(path)
    except Exception as e:
        print("no such path found")

