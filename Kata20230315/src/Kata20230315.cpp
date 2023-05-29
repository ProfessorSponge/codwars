//============================================================================
// Name        : Kata20230315.cpp
// Author      : Will Floyd
// Version     : 1
// Copyright   : no
// Description : https://www.codewars.com/kata/63f96036b15a210058300ca9
//============================================================================

/*In this kata, you need to write a function that takes a string and a letter as input and
 * then returns the index of the second occurrence of that letter in the string.
 * If there is no such letter in the string, then the function should return -1.
 * If the letter occurs only once in the string, then -1 should also be returned.

Examples:

second_symbol('Hello world!!!','l') --> 3
second_symbol('Hello world!!!', 'A') --> -1

Good luck ;)
*/


#include <iostream>
#include <cstring>
#include <string>
using namespace std;

int main() {
	string phrase;
	string target;

	int plength;
	bool oneplus = 0; 	//true after the first target letter has been found
	int tarpos = -1;	//position of the target character

	cout << "Enter First String" << endl;
	cin >> phrase;
	cout << "Enter target character" << endl;
	cin >> target;

	plength=phrase.size();
	char* phrasechar = new char[plength];
	char* tarchar = new char[1];

	strcpy(phrasechar, phrase.c_str());
	strcpy(tarchar, target.c_str());

	for(int i = 0; i < plength; i++){
		if(phrasechar[i] == tarchar[0])
			if(!oneplus){
				oneplus = 1;
			} else {
				tarpos=i;
				cout << to_string(tarpos);
				return tarpos;
			}
	}
	if(!oneplus || tarpos==-1){	// return -1 if no targets were found
		cout << "-1";
		return -1;
	}

	return -1;
}

