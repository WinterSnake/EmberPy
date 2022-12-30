/*
    Ember Debug Functions
    Compiled from C
*/
#include <unistd.h>
#define BUFFER_CAPACITY 32

void __PRINTU__(unsigned long long int x)
{
    char buffer[BUFFER_CAPACITY];
    unsigned short int buffer_size = 1;
    buffer[BUFFER_CAPACITY - 1] = '\n';
    do
    {
        buffer[(BUFFER_CAPACITY - 1 - (buffer_size++))] = x % 10 + '0';
        x /= 10;
    } while (x);
    write(1, &buffer[BUFFER_CAPACITY - buffer_size], buffer_size);
}

int main()
{
    __PRINTU__(10974123);
    __PRINTU__(1937);
    __PRINTU__(420);
    __PRINTU__(69);
    __PRINTU__(0);
    return 0;
}
