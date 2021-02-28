using namespace std;
#include <iostream> 
#include <vector> 

#ifndef NODE_H
#define NODE_H

class Node 
{   
public:
   char boolean_name;
   int level;
   vector<char> outgoing_connections;
   
   Node(char name, int l, vector<char> arcs);
};
 
#endif