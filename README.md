# BayesianProbReasoning

**Assignment:** AI Group Project, BayesianProbReasoning

**Course:** CSE 4301, Spring 2021

**Students:** Calvin Burns `cburns2017@my.fit.edu`, Carlos Cepeda `ccepeda2018@my.fit.edu`

## Dependencies 

This project uses Python. Any install of Python > version 3 will work.

On most systems, a python virtual environment should be created to run the project. If you have python and pip installed, you can use [venv](https://docs.python.org/3/library/venv.html#module-venv).

Once you have a version of python setup, you can install the required dependency, `numpy`. 

To do this, run: `pip install numpy`

## Compile and Run

Compile and Run: `python main.py`

## Sample Input/Output


**Input Network:**
```
example_network = BayesNet([
        ('Burglary', '', 0.001),
        ('Earthquake', '', 0.002),
        ('Alarm', 'Burglary Earthquake', {(True, True): 0.95, (True, False): 0.94, (False, True): 0.29, (False, False): 0.001}),
        ('JohnCalls', 'Alarm', {True: 0.90, False: 0.05}),
        ('MaryCalls', 'Alarm', {True: 0.70, False: 0.01})
    ])
```


**Run `enum_ask` for query `P(JohnCalls|MaryCalls)`:**
```
ans_dist = enum_ask('JohnCalls', {'MaryCalls': True}, example_network)
print(ans_dist)
```


**Output of `ans_dist`:**
```
P(JohnCalls|MaryCalls) = {True: 0.1775766000872957, False: 0.8224233999127043}
```


## Class Design :package:

After phase 1.1, we realized we had some fundamental issues with our implementation. We originally tried to use cpp vectors and rudimentary dictionary structures. When we went to implement the enumeration and query algorithms, we realized our implementation would cause a lot of headaches.

We chose to rewrite our code in Python so we could utilize Python's built-in dictionary and tuple data structures. It also saved us a lot of pain with data type mismatches we ran into before(specifically between source nodes and conditional nodes). The conversion to Python allowed us to have only 1 node class. When choosing a format for saving our data, I consulted the resources below for recommended implementations.

We have 3 classes implemented:

### 1. `BayesNet`

This object represents a bayesian network. It is comprised of a list of `Node`s and a list of variable names. 

The object has 2 methods. The first is `add_node` which takes a `Node`-like data structure(i.e. `('name', 'parents', table)`), creates a new node, and adds it to the network. The second method is `get_node` which takes a variable name and returns the corresponding `Node` object.

**Retrospection:** Our C++ implementation of the `BayesNet` was just a vector(i.e. list). We planned to create a class to implement the `BayesNet` during this phase and did it during the conversion to Python.


### 2. `Node`

This object represents a node in a `BayesNet` object. It is comprised of a variable name, children, parents, and a table that represents a conditional probability table.

A `table` has 2 forms. For source nodes, only an integer is passed. For conditional nodes, a dictionary representation is passed. The keys in the dictionary are Python `tuples` containing coresponding `boolean` values for each parent in `self.parents`.

**Retrospection:** This design was very close to our C++ implementation. The main difference is that we were using vectors parallel vectors to store the boolean values and their probability values. Using the `{tuple: value}` structure of the dictionary allows for easy accessing.

### 3. `Distribution`

This object represents a distribution over the query variable. It was inspired by the use of a *"distribution over X"* in the Enumerate-Ask algorithm from the textbook(Figure 14.9). 

The object is dynamically programmed so it could hold more than 2 values but for the purpose of this problem, it only holds `True` and `False` with corresponding probability values. To fetch a single one of these values use `dictionary[True]` or `dictionary[False]`.

The main purpose of the `Distribution` object is the `normalize` method. I followed the textbooks formula for normalization from Chapter 13.9.

**Resources Used:**

- Textbook Chapters 13 and 14
- https://github.com/aimacode/aima-python
- https://github.com/sonph/bayesnetinference/blob/master/BayesNet.py
