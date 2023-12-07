The states
1) S0 represents the stage before the smart contract is deployed or after deploying party has quit or aborted
the transaction and funds are transferred back to him.
2) S1 represents the stage just after the smart contract is deployed and Alice’s fund is locked.
3) S2 represents the stage after freeze function is called.
4) S3 represents the stage after funds is transferred to the
other party.
It is important to

state p can move to state q as follows

x1 can always change from 0 to 1
y1 can always change from 0 to 1
x1 cannot change from 1 to 0
y1 cannot change from 1 to 0
x2 cannot change from 1 to 0
y2 cannot change from 1 to 0

s1 can always go from 0 to 1
s2 can always go from 0 to 1
if s1 goes from 1 to 0, then a must also become 1
if s2 goes from 1 to 0, then b must also become 1

if s1 goes from 1 to 2, then x1, y1,y2 must also become 1
if s2 goes from 1 to 2, then y1, x1, x2 must also become 1

if s1 goes from 2 to 0, then b must become 1
if s2 goes from 2 to 0, then a must become 1

if s1 goes from 2 to 3, then x1, x2, y1, y2 must also become 1
if s2 goes from 2 to 3, then x1, x2, y1, y2 must also become 1


S1 -> S2 (x1,y1,y2)