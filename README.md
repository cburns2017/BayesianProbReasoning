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

## Class Design :package:

After phase 1.1, we realized we had some fundamental issues with our implementation. We originally tried to use cpp vectors and rudimentary dictionary structures. When we went to implement the enumeration and query alogirthms, we realized our implementation would cause a lot of headaches.

We chose to rewrite our code in Python so we could utilize Python's built-in dictonary and tuple datastructures. It also saved us a lot of Pain with datatype mismatches we ran into before. The conversion to Python allowed us to have only 1 node class. When choosing a format for saving our data, I consulted the resources below for recommended implementations.

**Resources Used:**

- https://github.com/aimacode/aima-python
- https://github.com/sonph/bayesnetinference/blob/master/BayesNet.py

## Sample Input/Output


**Input Network:**
```
example_network = BayesNet([
        ('Burglary', '', 0.001),
        ('Earthquake', '', 0.002),
        ('Alarm', 'Burglary Earthquake', {(T, T): 0.95, (T, F): 0.94, (F, T): 0.29, (F, F): 0.001}),
        ('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
        ('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
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
