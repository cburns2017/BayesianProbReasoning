# BayesianProbReasoning

Project for AI, CSE 5290

## Dependencies 

This project uses Python. Any install of Python > version 3 will work.

On most systems, a python virtual environment should be created to run the project. If you have python and pip installed, you can use [venv](https://docs.python.org/3/library/venv.html#module-venv).

Once you have a version of python setup, you can install the required dependency, `numpy`. 

To do this, run: `pip install numpy`

## Compile and Run

Compile and Run: `python main.py`

## Class Design :package:

After phase 1.1, we realized we had some fundamental issues with our implementation. We originally tried to use cpp vectors and rudimentary dictionary structures. When we went to implement the enumeration and query alogirthms, we realized our implementation would cause a lot of headaches.

We chose to rewrite our code in Python so we could utilize Python's built-in dictonary and tuple datastructures. It also saved us a lot of Pain with datatype mismatches we ran into before. The conversion to python allowed us to have only 1 node class. When choosing a format for saving our data, I consulted the resources below for recommended implementations.

Resources Used:
https://github.com/aimacode/aima-python
https://github.com/sonph/bayesnetinference/blob/master/BayesNet.py