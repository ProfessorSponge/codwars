#include <string>
#include <iostream>



std::string even_or_odd(int number) 
{
  if ( (number % 2) == 0){
    return "Even";
  } else {
    return "Odd";
  }
}


int main(int argc, char* argv[])
{
    std::string result;
    int counter = 99;
    while (counter > 0){
      result = even_or_odd(counter);
        std::cout << result;
        std::cout << std::endl;
        counter--;
    }
    
    
}

