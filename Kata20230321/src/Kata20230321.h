/*
 * Kata20230321.h
 *
 *  Created on: 21 Mar 2023
 *      Author: will
 */

#ifndef SRC_KATA20230321_H_
#define SRC_KATA20230321_H_
#include <iostream>
#include <cstring>
#include <string>
#include <sstream>
#include <vector>
using namespace std;

class Kata20230321 {
};

string spinner(string strin){
	//vector<string>
	string delim = " ";
	string token;
	vector<string> split;
	size_t poss, posnd, delimlen = delim.length();

	while ((posnd = strin.find(delim, poss)) != string::npos){
		token = strin.substr(poss, posnd - poss);
		poss = posnd + delimlen;
		split.push_back(token);
	}

	split.push_back(strin.substr(poss));


	//string token = strin.substr(0, s.find(" "));
	string outstr = "";
	for (auto strig:split){
		//cout <<strig.length();
		if (strig.length() >= 5){
			string invertd = "";
			for (int i = strig.length()-1; i>=0; i--){
				invertd.push_back(strig.at(i));
			}
			outstr.append(invertd);
		} else {
			outstr.append(strig);
		}
		outstr.append(" ");
	}


	return outstr;
}
//string spinner(string strin){

#endif /* SRC_KATA20230321_H_ */
