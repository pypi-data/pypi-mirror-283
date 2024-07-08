# Using gurobi syntax for MIP modeling

The syntax of gurobi is very traversal for mip modeling, but the syntax of some open-source solvers and their corresponding API interfaces often uses the conventional naming convention of Python, which is inconvenient for programming with complex constraints.

Therefore, I developed a Python library called gurobi2, which encapsulates commonly used objects such as variable sets, create constraints, constraint sets, and large M methods, and provides a programming experience consistent with gurobipy. I hope to improve the efficiency and experience of programming through this.

For specific API usage, please refer to the official documentation of Gurobi: https://www.gurobi.com/documentation/current/refman/index.html