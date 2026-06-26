<h1>Inductive Miner Concurrency</h1>

This Project contains an extended Version of the basic Inductive Miner. 
Instead of total ordered Traces this Version uses partial ordered traces as input.

Inductive Miner (Log(trace(ordered activities))) → Process Tree
IM-Concurrency (Log(trace(activities, directly follows relation))) → Process Tree

The discovered Process Tree also has partial ordered semantics instead of 
the total ordered semantics Process Tree discovered by traditional Inductive Miner.