import subprocess
from subprocess import PIPE

class Shell:
    def __init__(self):
        self.process = subprocess.Popen(['/home/jamie/if/glulxe/glulxe',
                '/home/jamie/Downloads/counterfeit-monkey.gblorb'], stdin=PIPE, stdout=PIPE)

    def readUntilBlocking(self):
        result = ""
        while True:
            line = self.process.stdout.readline()
            if line == 'blocking on input...\n':
                break
            result += line
            print(line)
        return result

    def runCommand(self, command):
        self.process.stdin.write(command)

shell = Shell()
print(shell.readUntilBlocking())
shell.runCommand("yes\n")
print(shell.readUntilBlocking())
