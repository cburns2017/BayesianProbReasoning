// AI Project

#include <iostream>
#include <vector> 
#include "node.h"
#include "source_node.h"

using namespace std;

int main()
{
   cout << "Hello World!" << endl;
   vector<char> vec; 
   vec.push_back('B');
   vec.push_back('X');
   int l = 0;
   int name = 'A';

   Node testNode = Node(name, l, vec);
   cout << testNode.boolean_name;
   cout << testNode.outgoing_connections.size() << endl;

   vector<char> vec2; 
   vec.push_back('W');
   vec.push_back('Y');
   l = 5;
   name = 'X';
   double prob = 0.13;
   
   SourceNode secondTest = SourceNode(name, l, vec, prob);
   cout << secondTest.boolean_name << secondTest.level << secondTest.prior_probability << endl;


}