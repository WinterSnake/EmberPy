#include "printf.c"
#include "printi.c"
#include "printu.c"

int main()
{
	// Ints
	PRINTINT(0);  // 0 test
	PRINTINT(-128);  // int8 MIN
	PRINTINT(127);  // int8 MAX
	PRINTINT(-32768);  // int16 MIN
	PRINTINT(32767);  // int16 MAX
	PRINTINT(-2147483648);  // int32 MIN
	PRINTINT(2147483647);  // int32 MAX
	PRINTINT(-9223372036854775807 - 1);  // int64 MIN
	PRINTINT(9223372036854775807);  // int64 MAX
	// UInts
	PRINTUINT(0);  // 0 test
	PRINTUINT(255);  // uint8 MAX
	PRINTUINT(65535);  // uint16 MAX
	PRINTUINT(4294967295);  // uint32 MAX
	PRINTUINT(18446744073709551615U);  // uint64 MAX
}
