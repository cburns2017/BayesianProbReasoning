# BayesianProbReasoning

Project for AI, CSE 5290

## :wrench:Compilation Instructions

Compile project: `g++ main.cpp source_node.cpp node.cpp`

Run code: `./a.out`

## :package:Class Design

3 node type classes have been created:

1. `Node` acts as the abstract base class for all node types in our program.
2. `SourceNode` represents nodes that do not have a probability table and only have a prior probability value.
3. `ConditionalNode` represents nodes with a probability table.