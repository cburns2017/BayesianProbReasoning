using namespace std;
#include <iostream> 
#include <vector>
#include <cmath>
#include "node.h"

#ifndef CONDITIONALNODE_H
#define CONDITIONALNODE_H

class ConditionalNode: public Node
{   
public:
    int num_vars;
    vector<char> table_headers;
    vector<string> bool_values;
    vector<double> prob_values;

    ConditionalNode(char name, int l, vector<char> arcs, int num_vars, vector<char> table_hdrs, vector<string> bool_vals, vector<double> prob_vals): Node(name, l, arcs) {
        table_headers = table_hdrs;
        bool_values = bool_vals;
        prob_values = prob_vals;
    };

    void print_table() {
        //print table
        for (int i = 0; i < num_vars; ++i) {
            cout << table_headers[i] << " ";
        }
        cout << "P(" << boolean_name << "|";
        for (int i = 0; i < num_vars; i++) {
            if(i + 1 != num_vars){
                cout << table_headers[i] << ",";
            } else {
                cout << table_headers[i];
            }
        }
        cout << ")" << endl;
        for (int j = 0; j < pow(2,num_vars); ++j) {
            cout << bool_values[j] << " " << prob_values[j] << endl;
        }
    };
};
 
#endif