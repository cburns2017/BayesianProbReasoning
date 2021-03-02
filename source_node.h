using namespace std;
#include <iostream> 
#include <vector> 
#include "node.h"

#ifndef SOURCENODE_H
#define SOURCENODE_H

class SourceNode: public Node
{   
public:
   double prior_probability;

   SourceNode(char name, int l, vector<char> arcs, double prior_prob): Node(name, l, arcs) { prior_probability = prior_prob; };

   void print_table(){
       cout << "P(" << boolean_name << ")" << endl;
       cout << prior_probability << endl;
   }
};
 
#endif