#include <iostream>
#include <random>



int main(){

 std::string message;/**/
 std::mt19937 generator;
 std::uniform_int_distribution<int> distrib(0,121);

	 do{
	 std::getline(std::cin,message);
	 std::cout<<"move:";
     std::cout<<distrib(generator)<<"\n";
	 }while(message!="kill");



 return 0;

}
