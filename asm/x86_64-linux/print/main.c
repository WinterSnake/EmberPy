/*
	Ember Debug Functions: Testing
	- Print
*/
#include "printf.c"
#include "printi.c"
#include "printu.c"

int main(int argc, char** argv)
{
    __PRINTU__(0);  // 0 test
    __PRINTU__(255);  // uint8 MAX
    __PRINTU__(65535);  // uint16 MAX
    __PRINTU__(4294967295);  // uint32 MAX
    __PRINTU__(18446744073709551615U);  // uint64 MAX
    __PRINTI__(0);  // 0 test
    __PRINTI__(-128);  // int8 MIN
    __PRINTI__(127);  // int8 MAX
    __PRINTI__(-32768);  // int16 MIN
    __PRINTI__(32767);  // int16 MAX
    __PRINTI__(-2147483648);  // int32 MIN
    __PRINTI__(2147483647);  // int32 MAX
    __PRINTI__(-9223372036854775807 - 1);  // int64 MIN
    __PRINTI__(9223372036854775807);  // int64 MAX
}
