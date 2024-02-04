# Atomic Swap

this repo aims to create the kripke structure for the atomic swaps and then try validate the kripke structure,

# How to run
Execute
```
python atomic_swap.py
```
And it should return the result on the terminal
# Current smart contracts and flow
## Deploy
Deploys the contract
## Init (x_1, x_2, a, y_1, y_2, b)

Initialize the code
* Can be merged with the deployment
* Cab be kept different to show different statees
* **Also need the address of the other party to transfer the amount**

## Freeze (x_1, y_1, y_2):
Freeze the smart contract. 
* Cannot quit
* Can abort, if other party has quit
## Quit(a)
quit the swap
* Only possible if the contract has not been frozen

## Abort(a,b)
abort the contract
* can be called if the other party has called the quit
  * Why is then a needed?



# Remove-x1 Branch
This Branch aims to test the code in case the variable x1 and y1 are not used. 

# Possible problems
1. how to initiate the change
