if [ -z "$1" ];
then
    echo "Building.."
    #  -Output Assembly
    gcc -S -masm=intel -Os -nostartfiles -no-pie -fno-stack-protector -fno-asynchronous-unwind-tables debug_functions.c -o debug_functions.s
    #  -Output Executable
    gcc debug_functions.c -o debug_functions
elif [ "$1" == "-C" ] || [ "$1" == "--clean" ];
then
    echo "Cleaning.."
    rm debug_functions
    rm debug_functions.s
fi
