# optimistic
A Python package for transforming specifications of optimization problems in various forms into code for
mathematical-optimization solvers (IBM CPLEX OPL) and heuristic solvers (RedHat OptaPlanner), as an attempt
to make decision optimization accessible to SMEs and developers who are not optimization experts and may not be
able to create efficient specfications for mathematical or heuristic solvers.

This project contains three tools, with different inputs and outputs.

* `validator2solver`: A developer (with the help of an SME) can write a functional Python program that checks whether a given 
solution satisfies the problem constraints, and computes the value of the objective function (possibly as a sum of
several objectives, each with an appropriate weight).  The tool converts this code into a specification for IBM CPLEX
that will enable the CPLEX solver to find an optimal solution.
* `scenoptic`: An SME creates a scenario in a spreadsheet, with appropriate (boolean-valued) formulas that evaluate
the problem constraints, and a formula that computes the objective function.  The tool converts this scenario into
a specification for IBM CPLEX or for RedHat OptaPlanner that will enable the solver to find an optimal solution.
* `eco_profiles`: This is an example of how to take a specification in a controlled natural language and convert it into
Python code that computes the value defined by the specification.  This code can then be incorporated into a problem
checker for `validator2solver`.

The analysis and transformations are all done using the mathematical and logical manipulation tools in the
[formalite](https://github.com/IBM/formaliter) project.

All content in this repository including code has been provided by IBM under the associated open source software license and IBM is under no obligation to provide enhancements, updates, or support. IBM developers produced this code as an open source project (not as an IBM product), and IBM makes no assertions as to the level of quality nor security, and will not be maintaining this code going forward.
