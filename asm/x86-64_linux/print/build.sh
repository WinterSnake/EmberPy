#!/bin/sh
if [ -z "$1" ]
then
	echo "Building.."
    # Build assembly
	gcc -S -Os -masm=intel -nostartfiles -no-pie -fno-stack-protector -fno-asynchronous-unwind-tables "printi.c" -o "printi.s"
	gcc -S -Os -masm=intel -nostartfiles -no-pie -fno-stack-protector -fno-asynchronous-unwind-tables "printu.c" -o "printu.s"
	# Build test
	gcc main.c -o print.x86-64
elif [ "$1" == "-c" ] || [ "$1" == "--clean" ]
then
	echo "Cleaning.."
	rm print*.s
	rm print.x86-64
fi
