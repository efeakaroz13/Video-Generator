#include <iostream>
#include <cstring>

using namespace std;

int main ()
{

	//1st way to get the MAC address
	

	//2nd way to get MAC address
	string str2 = "ifconfig en0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' "; 

	const char *command2 = str2.c_str();



		system(command2);

	return 0;
}