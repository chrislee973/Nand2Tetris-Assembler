
import sys
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

if __name__ == '__main__':
    input = sys.argv[1]
    f = Parser(input)
    c = Code()
    s = SymbolTable()

    # counter which tells us which instruction line we're on (ignores label declarations)
    instruct_counter = 0

    while f.hasMoreCommands():

        current = f.current_command

        # Chek if current command is L command
        if f.commandType(current) == 'L_COMMAND':
            # Get the symbol for the L command
            symbol = f.get_symbol(current)

            # Get the address of next command
            address = instruct_counter
            s.addEntry(symbol, address)
            f.advance()
            continue

        instruct_counter += 1
        f.advance()

    # Second Pass
    # Reset Parser object
    f = Parser(input)

    with open(sys.argv[2], 'w') as test:

        # Initialize starting variable address space
        var_address = 16

        while f.hasMoreCommands():

            current = f.current_command

            # Chek if current command is A command
            if f.commandType(current) == 'A_COMMAND':
                # Get the symbol for the A command
                symbol = f.get_symbol(current)

                # Check if symbol is numeric or not.
                # If it is, directly encode the number into binary and write to output file
                if symbol.isnumeric():
                    test.write(c.encode_symbol(symbol))
                    test.write('\n')
                # If not, check if if the symbol is in the symbol table.
                else:
                    # If it is, it's an L command and it'll already be in symbol-table
                    if s.contains(symbol):
                        address = s.getAddress(symbol)

                        # Encode address to binary
                        address = c.encode_symbol(address)

                        # Write to output file
                        test.write(address)
                        test.write('\n')

                    # If not, then it's a variable and assign it the next available address in variable address space
                    else:
                        s.addEntry(symbol, var_address)
                        address = s.getAddress(symbol)

                        # Encode address to binary
                        address = c.encode_symbol(address)

                        # Write to output file
                        test.write(address)
                        test.write('\n')

                        # Increment var_address for next unassigned variable
                        var_address += 1

                        # If current command is C command:
            elif f.commandType(current) == 'C_COMMAND':
                dest = f.get_dest(current)
                dest = c.encode_dest(dest)

                comp = f.get_comp(current)
                comp = c.encode_comp(comp)

                jump = f.get_jump(current)
                jump = c.encode_jump(jump)

                test.write(f"111{comp + dest + jump}")
                test.write('\n')

            f.advance()

