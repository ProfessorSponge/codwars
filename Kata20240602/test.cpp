#include <iostream>
#include <string>
#include <vector>
#include <map>




std::string solution(int number){
	// convert the number to a roman numeral
	std::string out = ""; 
	
	std::vector<int> nums = {1000, 500, 100, 50, 10, 5, 1};
	std::vector<std::string> chars = {"M", "D", "C", "L", "X", "V", "I"};

	//for (auto pair : romanChars){
	for (int i = 0; i < nums.size(); i++){
		int current = nums[i];
		if (number >= current){
			std::cout << nums[i];
			int repeats = number/current;
			std::cout << " repeats: " << repeats << std::endl;
			if (repeats == 0){
			} else if (repeats < 4){
				for (int j=0; j<repeats; j++){
					out.append(chars[i]);
				}
			} else {
				out.append(chars[i]);
				out.append(chars[i+1]);
			}
			
			number = number - current * repeats;
		}
	}

	return out;
}

//1 to 3999 



int main() {
	//int start = 3990;
	//int end = 3999;

	//for (int i = start; i < end; i++){
	//	std::cout << i << solution(i) << std::endl;
	//}
	

	//std::cout << 3999 << std::endl;
	std::cout << solution(182) << std::endl;
	std::cout << solution(1990) << std::endl;
	std::cout << solution(1875) << std::endl;
	
	return 0;
}


