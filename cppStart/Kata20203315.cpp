/*
 * Kata2023315.cpp
 *
 *  Created on: 15 Mar 2023
 *      Author: will
 */





#include <iostream>
#include <string>
#include "Kata20203315.h"

using namespace std;

int main() {
    string p1;
    string p2;

	cout << "pls enter two digits and press return" << endl;
    cin >> p1 >> p2;

	int prod;
	prod = product(stoi(p1),stoi(p2));

	cout << to_string(prod) << endl;
    return 0;
}
