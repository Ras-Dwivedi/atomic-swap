from KripkeStructure import KripkeStructure
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

# Get the label of a state
print("Label of s1:", kripke.get_label("s1"))
print("Label of s2:", kripke.get_label("s2"))
print("Label of s3:", kripke.get_label("s3"))

# Print the Kripke structure
print(kripke)