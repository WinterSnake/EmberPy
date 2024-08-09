/*
	Ember Debug Functions
	- Print uint
*/
#include <unistd.h>
#ifdef BUFFER_CAPACITY
	#undef BUFFER_CAPACITY
#endif
#define BUFFER_CAPACITY 32

void __PRINTU__(unsigned long long int x)
{
    char buffer[BUFFER_CAPACITY];
    unsigned short int bufferSize = 1;
    buffer[BUFFER_CAPACITY - 1] = '\n';
    do
    {
        buffer[BUFFER_CAPACITY - 1 - (bufferSize++)] = x % 10 + '0';
        x /= 10;
    } while (x);
    write(1, &buffer[BUFFER_CAPACITY - bufferSize], bufferSize);
}
