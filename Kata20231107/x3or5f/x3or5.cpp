//Multiples of 3 or 5

/*If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Finish the solution so that it returns the sum of all the multiples of 3 or 5 below the number passed in.

Additionally, if the number is negative, return 0.

Note: If the number is a multiple of both 3 and 5, only count it once.
*/

#include <iostream>

using namespace std;

int solution(int number) 
{
    number--;
    int sum = 0;
    while (number > 0){
        if ((number%3==0) || (number%5==0)){
            sum+=number;
        }
        number--;
    }
    return sum;
}



int main(int argc, char* argv[]){
    int nums = 100;
    while (nums > 0){
        cout << nums << ": " << solution(nums) << endl;
        nums--;
    }
    return 0;
}
