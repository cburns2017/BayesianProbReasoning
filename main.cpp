// AI Project: BayesianProbReasoning
// CSE 4301, Sprint 2021
// Calvin Burns (cburns2017@my.fit.edu) and Carlos Cepeda (ccepeda2018@my.fit.edu)

// Compile: g++ main.cpp source_node.cpp conditional_node.cpp node.cpp
// Run: ./a.out

// See node.h, source_node.h, and conditional_node.h for our node objects.
// Currently using a vector to store all the nodes in the network. Nodes
// have pointers to their outgoing connections so we can traverse the network via those.

// A template for our input file is available in input_template.txt.

#include <iostream>
#include <vector>
#include <fstream>
#include <cstdlib>
#include <math.h>
#include <string>
#include "node.h"
#include "source_node.h"
#include "conditional_node.h"

using namespace std;

int main()
{
    cout << "Hello World!" << endl;
    ifstream myfile; //Input file
    myfile.open("inputv2real.txt");
    vector<Node> bay_net; //Bayesian Network data structure
    int total_nodes = 0;
    int total_levels = 0;
    //Source Nodes
    int level = 0;
    myfile >> level; //Reads in current level of the node
    cout << "Level: " << level << endl;
    int num_nodes;
    myfile >> num_nodes; //Reads in number of source nodes
    for(int i = 0; i < num_nodes; i++) //Reads in source nodes that are first in the file
    {
        char node_name;
        myfile >> node_name;
        total_nodes++;
        if(total_nodes > 10) //Checks for surplus of nodes
        {
            cout << "Error, too many source nodes!" << endl;
            exit(1);
        }
        double prior_prob;
        myfile >> prior_prob;
        int num_of_arcs; //Reads and checks the number of arcs
        myfile >> num_of_arcs;
        if(num_of_arcs > 15)
        {
            cout << "Error, too many arcs" << endl;
            exit(1);
        }
        vector<char> arcs; //Vector of edges new node will point to
        char temp;
        for(int j = 0; j < num_of_arcs; j++) //Adds the nodes that are being pointed to by new node
        {
            myfile >> temp;
            arcs.push_back(temp);
        }
        SourceNode baynode = SourceNode(node_name, level, arcs, prior_prob); //Initialize source nodes
        bay_net.push_back(baynode); //Add source node to network
        baynode.print_table();
    }
    //Conditional Nodes
    while(!myfile.eof()) //Will loop until all conditional nodes have been inputted
    {
        myfile >> level; //Gets and checks the level of the next set of conditional nodes
        cout << "Level: " << level << endl;
        total_levels++;
        if(total_levels > 5)
        {
            cout << "Error, too many levels to graph" << endl;
            exit(1);
        }
        myfile >> num_nodes; //Gets and checks number of condtional nodes on the current level
        for(int i = 0; i < num_nodes; i++) //Loops through all condtional nodes on the current level
        {
            char node_name;
            myfile >> node_name;
            total_nodes++;
            if(total_nodes > 10)
            {
                cout << "Error, too many source nodes!" << endl;
                exit(1);
            }
            int num_var_in_table;
            myfile >> num_var_in_table;
            vector<char> table_headers; //These 3 vectors will be the table that is stored in condtional nodes
            vector<string> bool_values;
            vector<double> prob_values;
            for(int j = 0; j < num_var_in_table; j++) //Reads in all the table headers of current conditional node
            {
                char temp;
                myfile >> temp;
                table_headers.push_back(temp);
            }
            for(int k = 0; k < pow(2.0, num_var_in_table); k++) //Reads in all the boolean and probability values of the table
            {
                string tempS;
                myfile >> tempS;
                bool_values.push_back(tempS);
                double tempD;
                myfile >> tempD;
                prob_values.push_back(tempD);
            }
            int num_of_arcs; //Gets and checks the number of arcs between nodes
            myfile >> num_of_arcs;
            if(num_of_arcs > 15)
            {
                cout << "Error, too many arcs" << endl;
                exit(1);
            }
            vector<char> arcs; //Vector of edges new node will point to
            char temp;
            for(int j = 0; j < num_of_arcs; j++) //Adds the nodes that are being pointed to by new node
            {
                myfile >> temp;
                arcs.push_back(temp);
            }
            ConditionalNode baynode = ConditionalNode(node_name, level, arcs, num_var_in_table, table_headers, bool_values, prob_values); //Initializes conditional node
            baynode.print_table();
            bay_net.push_back(baynode); //Adds conditional node to network
        }
    }
    //finally, convert text relationships to pointer relationships
    for(int i = 0; i < bay_net.size(); i++) {
        bay_net[i].convert_connections(bay_net);
    }
    return 0;
}