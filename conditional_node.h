using namespace std;
#include <iostream> 
#include <vector> 
#include "node.h"

#ifndef CONDITIONALNODE_H
#define CONDITIONALNODE_H

class ConditionalNode: public Node
{   
public:
   double prior_probability;

   ConditionalNode(char name, int l, vector<char> arcs, double prior_prob): Node(name, l, arcs) { 
      prior_probability = prior_prob; 
      // TODO: add a way to store the probability table
      };
};
 
#endif