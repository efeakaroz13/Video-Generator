#include <iostream>
#include <cstring>

using namespace std;

int main ()
{

	string str2 = "ifconfig en0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}' "; 

	const char *macaddress = str2.c_str();



		system(macaddress);

	return 0;
}