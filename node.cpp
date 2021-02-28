#include "node.h"

Node::Node(char name, int l, vector<char> arcs) {
   boolean_name = name;
   level = l;
   outgoing_connections = arcs;
}