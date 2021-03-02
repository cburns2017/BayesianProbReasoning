// AI Project

#include <iostream>
#include <vector>
#include <cmath>
#include "node.h"
#include "source_node.h"
#include "conditional_node.h"

using namespace std;

int main()
{
    cout << "Hello World!" << endl;
//    vector<char> vec;
//    vec.push_back('B');
//    vec.push_back('X');
//    int l = 0;
//    char name = 'A';
//
//    Node testNode = Node(name, l, vec);
//    cout << testNode.boolean_name;
//    cout << testNode.outgoing_connections.size() << endl;
//
//    vector<char> vec2;
//    vec.push_back('W');
//    vec.push_back('Y');
//    l = 5;
//    name = 'X';
//    double prob = 0.13;
//
//    SourceNode secondTest = SourceNode(name, l, vec, prob);
//    cout << secondTest.boolean_name << secondTest.level << secondTest.prior_probability << endl;

    int l = 1;

    char name = 'A';
    vector<char> arcs;
    arcs.push_back('J');
    arcs.push_back('M');

    int num_vars = 2;
    vector<char> table_headers;
    vector<string> bool_values;
    vector<double> prob_values;
    table_headers.push_back('B');
    table_headers.push_back('E');
    bool_values.push_back("TT");
    prob_values.push_back(0.95);
    bool_values.push_back("TF");
    prob_values.push_back(0.94);
    bool_values.push_back("FT");
    prob_values.push_back(0.29);
    bool_values.push_back("FF");
    prob_values.push_back(0.001);

    ConditionalNode finalTest = ConditionalNode(name, l, arcs, num_vars, table_headers, bool_values, prob_values);
    finalTest.print_table();

}