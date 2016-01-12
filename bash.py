import subprocess
from subprocess import PIPE

class Shell:
    def __init__(self):
        self.process = subprocess.Popen(['/home/jamie/if/glulxe/glulxe',
                '/home/jamie/Downloads/counterfeit-monkey.gblorb'], stdin=PIPE, stdout=PIPE)

    def runCommand(self, command):
        self.process.stdin.write(command)
        result = ""
        while True:
            char = self.process.stdout.read(1)
            result += char
            print(char)
            if char == '>':
                break
        return result

shell = Shell()
print(shell.runCommand("yes\n"))
