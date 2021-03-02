using namespace std;
#include <iostream> 
#include <vector> 

#ifndef NODE_H
#define NODE_H

// Abstract Node Class
class Node 
{   
public:
   char boolean_name;
   int level;
   vector<char> outgoing_connections;
   vector<Node> real_connections;
   
   Node(char name, int l, vector<char> arcs);

   //convert text representation to pointer representation of network
   void convert_connections(vector<Node> bay_net) {
       vector<Node> temp;
       for (int i = 0; i < outgoing_connections.size(); i++) {
            //find the node
            for (int j = 0; j < bay_net.size(); j++) {
                if (bay_net[j].boolean_name == outgoing_connections[i]) {
                    temp.push_back(bay_net[j]);
                }
            }
       }
       real_connections = temp;
   }

};
 
#endif