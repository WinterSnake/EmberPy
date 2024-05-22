if [ -z "$1" ];
then
    echo "Building.."
    # -Output Assembly
	gcc -S -Os -masm=intel -nostartfiles -no-pie -fno-stack-protector -fno-asynchronous-unwind-tables "printf.c" -o "printf.asm"
	gcc -S -Os -masm=intel -nostartfiles -no-pie -fno-stack-protector -fno-asynchronous-unwind-tables "printi.c" -o "printi.asm"
	gcc -S -Os -masm=intel -nostartfiles -no-pie -fno-stack-protector -fno-asynchronous-unwind-tables "printu.c" -o "printu.asm"
	# -Build test
	gcc main.c -o print
elif [ "$1" == "-C" ] || [ "$1" == "--clean" ];
then
    echo "Cleaning.."
	rm print
	rm print*.asm
fi
