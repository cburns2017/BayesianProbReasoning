"""
Assignment: AI Project, BayesianProbReasoning, Phase 1.2
Course: CSE 4301, Spring 2021
Students: Calvin Burns (cburns2017@my.fit.edu), Carlos Cepeda (ccepeda2018@my.fit.edu)

Compile and Run: python main.py

---

After phase 1.1, we realized we had some fundamental issues with our implementation. We
originally tried to use cpp vectors and rudimentary dictionary structures. When we went
to implement the enumeration and query alogirthms, we realized our implementation would cause
a lot of headaches.

We chose to rewrite our code in Python so we could utilize Python's built-in dictonary and
tuple datastructures. It also saved us a lot of Pain with datatype mismatches we ran into before.
The conversion to python allowed us to have only 1 node class. When choosing a format for saving our
data, I consulted the resources below for recommended implementations.

Resources Used:
https://github.com/aimacode/aima-python
https://github.com/sonph/bayesnetinference/blob/master/BayesNet.py

---

Creating networks follow this pattern:

example_network = BayesNet([
        ('VariableName0', '', 0.001),
        ('VariableName1', '', 0.002),
        ('VariableName2', 'VariableName0 VariableName1',
         {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
        ...
    ])
VariableName0 and VariableName1 are prior probabilities. VariableName2 is a conditional probability 
with 0 and 1 as priors.

---

Enumeration ask returns a distribution like figure 14.9 from the textbook. To access the True or False
values, use list indice syntax as follows:

ans_dist[T] gives you the True value.
ans_dist[F] gives you the False value.
"""

import numpy as np

# Global Vars
T, F = True, False


def extend_e(e, var, val):
    """Copy and append value to dictionary.
    For example:
    e = {'JohnCalls': True, 'MaryCalls': True}
    var = 'NewVar'
    val = False
    The function returns:
    {'JohnCalls': True, 'MaryCalls': True, 'NewVar': False}
    """
    return {**e, var: val}


class Distribution:
    """
    Represents a discrete probability distribution.

    Used in the enumerate_ask function. In all cases, a prob dist
    object will have at most 2 values, the first is the positive, second
    is the negative value.

    Usage of the normalize function is what motivated the creation of this object.
    """

    def __init__(self, name=''):
        self.prob = {}
        self.name = name
        self.values = []

    def __getitem__(self, val):
        """Given a value, return P(value)."""
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        """Set P(val) = p."""
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """
        Get the normalized distribution.

        Follows example from text book in section 13.9 and the AIMA example code.
        """
        total = sum(self.prob.values())
        if not np.isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def __repr__(self):
        """
        Overwrites the string cast operation for a Distribution object
        """
        return "P({})".format(self.name) + " " + str(self.prob)


class Node:
    """
    Represents a single node in a BayesNet.

    Table is the conditional probability table.
    It takes a dictionary with a true/false tuple
    as keys and a float as values. Variable indices
    match 1-to-1 with the order of entries in the table.
    """

    def __init__(self, name, parents, table):
        self.variable = name
        self.children = []

        if isinstance(parents, str):
            parents = parents.split()
        self.parents = parents

        if isinstance(table, (float, int)):  # no parents, 0-tuple, evidence nodes
            table = {(): table}
        elif isinstance(table, dict): # some parents, n-tuple, conditional nodes
            if table and isinstance(list(table.keys())[0], bool):
                table = {(v,): p for v, p in table.items()}
        self.table = table

    def p(self, val, event):
        """
        Get value from table using val and observed events.
        tuple([event[var] for var in self.parents]) produces the
        parent values, the values of parents for the event node.

        If a val is not given, the inverse probability is returned.
        """
        truth_val = self.table[tuple([event[var] for var in self.parents])]
        if val:
            return truth_val
        else:
            return 1 - truth_val

    def __repr__(self):
        """
        Overwrites the string cast operation for a Node object
        """
        return repr((self.variable, ' '.join(self.parents)))


class BayesNet:
    """
    Bayesian network class. Composed of Nodes.
    During construction, parent nodes must precede children nodes in order of
    initialization.
    """

    def __init__(self, temp_nodes=None):
        self.nodes = []
        self.variables = []
        # get the temp nodes and add them using the add method
        temp_nodes = temp_nodes or []
        for temp_node in temp_nodes:
            self.add_node(temp_node)

    def add_node(self, temp_node):
        """
        Creates a node and adds it to the network.
        """
        # create a new node and add it to the network
        node = Node(*temp_node)
        self.nodes.append(node)
        # add node's variables to the network variables list
        self.variables.append(node.variable)
        # connect parent nodes to their newly created children
        for p in node.parents:
            self.get_node(p).children.append(node)

    def get_node(self, var):
        """
        Find and return the corresponding bay net node for the given name
        """
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("Variable does not exist: {}".format(var))

    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)


def enumerate_all(vars, e, bn):
    """
    For a given list of variables and list of observed variables, enumerate
    all combinations.

    Algorithm copied from textbook Fig 14.9.
    """
    if not vars:
        return 1.0
    Y, rest = vars[0], vars[1:]
    node = bn.get_node(Y)
    if Y in e:
        return node.p(e[Y], e) * enumerate_all(rest, e, bn)
    else:
        return sum(node.p(y, e) * enumerate_all(rest, extend_e(e, Y, y), bn) for y in [True, False])


def enumeration_ask(X, e, bn):
    """
    Given a query variable, observed values, and network, compute the conditional
    probability.

    Algorithm copied from textbook Fig 14.9.

    A distribution object is used to handle the storage and normalization of the probability.
    """
    Q = Distribution(X)
    for xi in [True, False]:
        Q[xi] = enumerate_all(bn.variables, extend_e(e, X, xi), bn)
    return Q.normalize()


def main():
    example_network = BayesNet([
        ('Burglary', '', 0.001),
        ('Earthquake', '', 0.002),
        ('Alarm', 'Burglary Earthquake',
         {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
        ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
        ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
    ])
    ans_dist = enumeration_ask('JohnCalls', {'MaryCalls': True}, example_network)
    print('P(JohnCalls|MaryCalls) = ' + str(ans_dist[T]))

if __name__ == "__main__":
    main()