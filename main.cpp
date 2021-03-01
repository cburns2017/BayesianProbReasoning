// AI Project

#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib> 
#include "node.h"
#include "source_node.h"

using namespace std;

int main()
{
   ifstream myfile; //Input file
   myfile.open("input.txt");
   vector<Node> BayNet; //Bayesian Network data structure
   
   int num_of_Snodes, num_of_Cnodes;
   myfile >> num_of_Snodes >> num_of_Cnodes; //Reads in # of source nodes and conditional nodes
   int total_nodes = num_of_Cnodes + num_of_Snodes;
   if(total_nodes < 7 || total_nodes > 10)
   {
      cout << "Error, number of nodes not within limits 7 and 10" << endl;
   }

   char bool_name;
   int depth, num_of_edges;
   double priorP;
   for(int i = 0; i < num_of_Snodes; i++) //Reads in source nodes that are first in the file
   {
      myfile >> bool_name;
      myfile >> priorP;
      myfile >> depth;
      myfile >> num_of_arcs;

      vector<char> arcs; //Vector of edges new node will point to
      char temp;
      for(int j = 0; j < num_of_arcs; j++) //Adds the nodes that are being pointed to by new node
      {
         myfile >> temp;
         arcs.push_back(temp);
      }

      SourceNode baynode = SourceNode(bool_name, depth, arcs, priorP); //Initialize source nodes
      BayNet.push_back(baynode); //Add source node to network
   }

   myfile >> num_of_Cnodes;

   for(int i = 0; i < num_of_Cnodes; i++)
   {
      
   }
}