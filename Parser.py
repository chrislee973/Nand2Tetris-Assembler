class Parser():

    # Initialize counter to index through the list of commands
    # counter = 0
    # current_command= ''

    def __init__(self, filename):
        # Read in input file
        with open(filename, 'r') as input:
            # Get a list of all the valid commands -- ignoring all white space/empty lines and comments
            commands = [line.strip() for line in input if line.split() and not line.strip().startswith('//')]

        self.counter = 0
        self.commands = commands
        self.current_command = self.commands[self.counter]

    def hasMoreCommands(self):
        return self.counter < len(self.commands)

    # Should be called only if hasMoreCommands() is True
    def advance(self):
        # Increment counter to select next command from commands list
        self.counter += 1
        if self.hasMoreCommands():
            # Set the new current command
            self.current_command = self.commands[self.counter]

    def commandType(self, current_command):
        # Check if A command
        if current_command.startswith('@'):
            return 'A_COMMAND'

        # CHeck if L command
        elif current_command.startswith('('):
            return 'L_COMMAND'

            # Check if C_COMMAND
        else:
            return 'C_COMMAND'

    # This method should be called only if current_command is A or L command
    # @staticmethod
    def get_symbol(self, current_command):

        # If the current_command is A command
        if self.commandType(current_command) == 'A_COMMAND':

            # Get everything past the '@' sign
            symbol = current_command[1:]

            return symbol

            # If the current_command is L command
        elif self.commandType(current_command) == 'L_COMMAND':
            # Get everything in between the two parentheses (the first and last symbols of the command)
            symbol = current_command[1:-1]

            return symbol

        else:
            return "Command is not A or L command"

    # These below methods called only if current_command is a C command
    def get_dest(self, current_command):

        # Check if dest field is populated
        if '=' in current_command:
            split_char = '='
            command = current_command.split(split_char)
            # dest is first element of split list
            dest = command[0]

            return dest

        # Else if the dest field is null (ie if '=' isn't in the current_command)
        else:
            return "null"

    def get_comp(self, current_command):

        # If jump field is missing
        if ';' not in current_command:
            # Split the command based off of '=' sign
            split_char = '='
            command = current_command.split(split_char)
            # comp is the second element of split list
            comp = command[1]

            return comp

            # If dest field is missing
        elif '=' not in current_command:
            split_char = ';'
            command = current_command.split(split_char)

            # comp is the first element of the split list
            comp = command[0]

            return comp

        # If dest and jump fields are present
        elif '=' in current_command and ';' in current_command:
            split_char = '='

            command = current_command.split(split_char)

            comp_jump = command[1]

            split_char = ';'

            command = comp_jump.split(split_char)

            comp = command[0]

            return comp

    def get_jump(self, current_command):
        # Check if jump field is populated
        if ';' in current_command:
            split_char = ';'
            command = current_command.split(split_char)
            # jump is second element of split list
            jump = command[1]

            return jump

        # Else if the jump field is null (ie if ';' isn't in the current_command)
        else:
            return "null"


if __name__ == '__main__':
    parse = Parser(sys.argv[1])
    print(parse.commands)