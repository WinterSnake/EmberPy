/*
	Ember Debug Functions
	- Print int
*/
#include <unistd.h>
#ifdef BUFFER_CAPACITY
	#undef BUFFER_CAPACITY
#endif
#define BUFFER_CAPACITY 32

void __PRINTI__(long long int x)
{
	char buffer[BUFFER_CAPACITY];
	unsigned short int bufferSize = 1;
    buffer[BUFFER_CAPACITY - 1] = '\n';
	int isNegative = x < 0;
	x = (x < 0) ? x * -1 - 1 : x;
	do
	{
        buffer[BUFFER_CAPACITY - 1 - (bufferSize++)] = x % 10 + '0' + (isNegative && bufferSize == 1 ? 1 : 0);
        x /= 10;
	} while (x);
	if (isNegative)
	{
        buffer[BUFFER_CAPACITY - 1 - (bufferSize++)] = '-';
	}
    write(1, &buffer[BUFFER_CAPACITY - bufferSize], bufferSize);
}
