from KripkeStructure import KripkeStructure, PathNotFoundError
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
                                        elif s2 == 3:
                                            label = "bad"
                                        else:
                                            label = "unknown"
                                    elif s1 ==1 :
                                        if s2 == 3:
                                            label = "bad"
                                        else:
                                            label = "unknown"
                                    elif s1==3:
                                        if s2 == 0:
                                            label = "bad"
                                        elif s2 == 3:
                                            label = "good"
                                        else:
                                            label = "unknown"
                                    elif s2==1:
                                        if s1 ==3:
                                            label = "bad"
                                        else:
                                            label = "unknown"
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

    # if a or b is revealed, the contract should stop executing further
    if a ==1 :
        if not s1 == new_s1:
            return False

    if b ==1:
        if not s2 == new_s2:
            return False

    #if contract is resolved, it should stop excuting
    if s1 ==3:
        if new_s1 != s1:
            return False
    if s2 == 3:
        if new_s2 != s2:
            return False

    # unless contract are deployed, no value can change:
    if s1 ==0 and s2 ==0:
        if new_a or new_b or new_x1 or new_x2 or new_y1 or new_y2:
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
    no_bad_states = kripke.count_states("bad")
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



def label_good_states(kripke):
    """
    labels all the good state in the kripke structure
    """
    for state in kripke.states:
        label_good_state(kripke, state)
    no_good_states = kripke.count_states("good")
    print(f"no of good states are {no_good_states}")
    # return no_good_states

def label_good_state(kripke, unknown_state):
    """
    marks the state as the good state if it can reach a good state in the future
    a state is good if it cannot be marked as bad
    """

    # a state marked as bad is already bad
    if kripke.get_label(unknown_state)=="bad":
        return False

    def dfs(state, visited_states):
        """
        returns True if any of the successor state is a good state
        else returns false
        """
        if state in visited_states:
            return

        visited_states.add(state)

        #if the state itself is good return True
        if kripke.get_label(state) == "good":
            # print(f'reached state {state}, which is good')
            return True

        #if the any of the sucessor is good, label it good
        for successor in kripke.get_successors(state):
            if dfs(successor, visited_states):
                return True

        return False

    visited_states = set()
    if dfs(unknown_state, visited_states):
        kripke.labels[unknown_state] = "good"




# Example usage:

def print_state(state):
    names = ['a', 'b', 'x1', 'x2', 'y1', 'y2', 's1', 's2']
    # state = enumerate(_state)
    for i in range(len(names)):
        print(f' {names[i]}={state[i] }', end="")
    print("\n")


def stats(kripke):
    good_states_count = kripke.count_states("good")
    bad_states_count = kripke.count_states("bad")
    unknown_states_count = kripke.count_states("unknown")

    print(f'Good states: {good_states_count}')
    print(f'Bad states: {bad_states_count}')
    print(f'unknown states: {unknown_states_count}')
    print(f"total states {good_states_count+bad_states_count+unknown_states_count}")



def count_states_with_labels(kripke, states_list):
    label_counts = {"good": 0, "bad": 0, "unknown": 0}

    for state in states_list:
        label = kripke.get_label(state)
        if label in label_counts:
            label_counts[label] += 1

    return label_counts

# def bad_reason(kripke, state):
#     """
#     prints the reason for  the state to be bad"
#     """
#     bad_states = [
#                     (0,0,0,0,0,0,0,0),
#                     (0,0,0,0,0,0,0,0),
#                     (0,0,0,0,0,0,0,0),
#                     (0,0,0,0,0,0,0,0),
                # ]
# Example usage:
if __name__ == "__main__":
    # Create a Kripke structure
    kripke = KripkeStructure()

    # Add states to the Kripke structure
    total_states = add_states_to_kripke(kripke)
    print(kripke.get_states_with_label("bad"))


    # Print the Kripke structure
    # print(kripke)

    # Output the total number of states inserted
    print("Total states inserted:", total_states)
    total_transition = add_transition_to_kripke(kripke)
    print("total transitions inserted", total_transition)
    print("labelling the bad states")
    label_bad_states(kripke)
    label_good_states(kripke)
    label_good_states(kripke)
    
    stats(kripke)
    print(kripke.get_label((0,0,0,0,0,0,0,0)))


    #if the state is bad, print the path

    states_reachable = kripke.find_reachable_states((0,0,0,0,0,0,0,0))
    print(states_reachable)
    print(count_states_with_labels(kripke,states_reachable))

    unknown_states = [state for state in states_reachable if kripke.get_label(state)=="unknown"]
    print("unknown states ")
    print(unknown_states)

    print("--------------")
    interesting_state = (0, 1, 1, 0, 1, 0, 1, 0)
    s = kripke.find_reachable_states(interesting_state)
    print(f"state inquired {interesting_state}")
    print(s)
    print(count_states_with_labels(kripke,s))
    # label_bad_state(kripke,(0,0,0,0,0,0,0,0))
    # print(kripke.get_label((0,0,0,0,0,0,0,0)))
    # # print(kripke.get_successors((0,0,0,0,0,0,0,0)))

    try:
        s1 = (0,0,0,0,0,0,0,0)
        # s2 = (0,0,0,0,0,0,0,3)
        s2 =  (1, 1, 1, 1, 1, 1, 0, 3)
        path = kripke.find_transition_path(s1, s2)
        for state in path:
            print_state(state)
        # print(path)
    except Exception as e:
        print("no such path found")

