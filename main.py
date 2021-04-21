"""
Assignment: AI Project, BayesianProbReasoning, Phase 1.2
Course: CSE 4301, Spring 2021
Students: Calvin Burns (cburns2017@my.fit.edu), Carlos Cepeda (ccepeda2018@my.fit.edu)

Compile and Run: python main.py

---

See README.md for full details on installation and class structure.

---

Create networks following this pattern:

example_network = BayesNet([
        ('VariableName0', '', 0.001),
        ('VariableName1', '', 0.002),
        ('VariableName2', 'VariableName0 VariableName1', {(True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001}),
        ...
    ])

VariableName0 and VariableName1 are prior probabilities. VariableName2 is a conditional probability
with 0 and 1 as priors.

---

Enumeration ask returns a distribution like figure 14.9 from the textbook. To access the True or False
values, use list indice syntax as follows:

ans_dist[True] gives you the True value.
ans_dist[False] gives you the False value.
"""

import numpy as np

"""
UTILITY FUNCTIONS
"""

def extend_e(e, var, val):
    """Copy dict and append value to new dict.
    For example:
    e = {'JohnCalls': True, 'MaryCalls': True}
    var = 'NewVar'
    val = False
    The function returns:
    {'JohnCalls': True, 'MaryCalls': True, 'NewVar': False}
    """
    new_dict = e.copy()
    new_dict[var] = val
    return new_dict


"""
CLASS/OBJECT DEFINITIONS
"""

class Distribution:
    """
    Represents a discrete probability distribution.

    Used in the enum_ask function. In all cases, a prob dist
    object will have at most 2 values, the first is the positive, second
    is the negative value.

    Usage of the normalize function is what motivated the creation of this object.
    """

    def __init__(self, name=''):
        self.prob = {}
        self.name = name
        self.values = []

    def __getitem__(self, val):
        """Get prob value using val as a key. Val will be True or False"""
        return self.prob[val]


    def __setitem__(self, val, p):
        """add a value to the prob dictionary"""
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
        return str(self.prob)


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

        if isinstance(table, (float, int)):  # no parents, evidence nodes
            # assign an empty table
            table = {(): table}
        elif isinstance(table, dict): # some parents, n-tuple, conditional nodes
            if table and isinstance(list(table.keys())[0], bool):
                # create table
                table = {(v,): p for v, p in table.items()}
        self.table = table

    def p(self, val, event):
        """
        Get value from table using val and observed events.
        tuple([event[var] for var in self.parents]) produces the
        parent values, the values of parents for the event node.

        Math syntax is similar to: P(A|e) or P(A)

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
        value = 'P(' + self.variable
        if self.parents:
            value = value + '|' + ', '.join(self.parents) + ')\n'
            value = value + str(self.parents) + '\n'
            for v, p in self.table.items():
                value = value + str(v) + ' \t' + str(p) + '\n'
        else:
            value = value + ')\n'
            for v, p in self.table.items():
                value = value + str(p) + '\n'
        return value


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
        value = ""
        for n in self.nodes:
            value += str(n) + '\n'
        return value


"""
ENUMERATION ALGORITHMS
"""

def enum_all(vars, e, bn):
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
        return node.p(e[Y], e) * enum_all(rest, e, bn)
    else:
        return sum(node.p(y, e) * enum_all(rest, extend_e(e, Y, y), bn) for y in [True, False])


def enum_ask(X, e, bn):
    """
    Given a query variable, observed values, and network, compute the conditional
    probability.

    Algorithm copied from textbook Fig 14.9.

    A distribution object is used to handle the storage and normalization of the probability.
    """
    Q = Distribution(X)
    for xi in [True, False]:
        Q[xi] = enum_all(bn.variables, extend_e(e, X, xi), bn)
    return Q.normalize()


"""
MAIN
"""

def main():
    # FLORIDA RED TIDE NETWORK
    florida_red_tide_network = BayesNet([
        ('Summer', '', 0.25),
        ('14DayAvgRainFall>3in', 'Summer', {True: 0.78, False: 0.22}),
        ('14DayAvgWaterTemp>80F', 'Summer', {True: 0.82, False: 0.18}),
        ('14DayAvgWindSpeed<10MPH', 'Summer', {True: 0.52, False: 0.48}),
        ('DischargeFromOkeechobee', '14DayAvgRainFall>3in', {True: 0.98, False: 0.02}),
        ('RedTideEvent', '14DayAvgWaterTemp>80F 14DayAvgWindSpeed<10MPH DischargeFromOkeechobee', {
            (True, True, True): 0.32, 
            (True, True, False): 0.03, 
            (True, False, False): 0.02, 
            (False, True, True): 0.23, 
            (True, False, True): 0.27, 
            (False, False, True): 0.11, 
            (False, True, False): 0.01, 
            (False, False, False): 0.01,
        }),
    ])
    print('Florida Red Tide Bayesian Network:\n')
    ans_dist = enum_ask('RedTideEvent', {'Summer': True}, florida_red_tide_network)
    print('P(RedTideEvent|Summer) = ' + str(ans_dist))
    ans_dist = enum_ask('DischargeFromOkeechobee', {'RedTideEvent': True}, florida_red_tide_network)
    print('P(DischargeFromOkeechobee|RedTideEvent) = ' + str(ans_dist))
    ans_dist = enum_ask('RedTideEvent', {'Summer': True, '14DayAvgWaterTemp>80F': True, 'DischargeFromOkeechobee': False}, florida_red_tide_network)
    print('P(RedTideEvent|Summer, 14DayAvgWaterTemp>80F, 14DayAvgWindSpeed<10MPH, ~DischargeFromOkeechobee) = ' + str(ans_dist))
    # END FLORIDA RED TIDE NETWORK

if __name__ == "__main__":
    main()