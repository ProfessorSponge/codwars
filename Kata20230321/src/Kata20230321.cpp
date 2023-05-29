/*
 * Kata20230321.cpp
 *
 *  Created on: 21 Mar 2023
 *      Author: will
 */

// Write a function that takes in a string of one or more words, and returns the same string,
// but with all five or more letter words reversed (Just like the name of this Kata).
// Strings passed in will consist of only letters and spaces
// Spaces will be included only when more than one word is present.

#include "Kata20230321.h"

using namespace std;




int main() {
	string inputstr = "to";
	string outptstr = spinner(inputstr);

	cout << outptstr;
	return 22;
}



