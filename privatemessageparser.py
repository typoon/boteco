import importlib
import commands
import sys
from connection import Connection

class PrivateMessageParser:

    _modules = []
    
    def __init__(self):
        self._conn = Connection()

    def parse(self, data):
        # Example message
        # :Gilgamesh!~gilgamesh@some_ip PRIVMSG #gilgabot :cool story bro

        tokens = [el.strip() for el in data.split(" ")]
        
        nick  = data[1:data.find("!")]
        to    = tokens[2]
        cmd   = tokens[3].lstrip(":").lstrip("!")

        if len(tokens) >= 4:
            param = [nick, to, " ".join(tokens[4:])]
        else:
            param = [nick, to]


        # Pre-defined commands
        if cmd == "list":
            self._list(to)
            return

        elif cmd == "quit":
            self._quit(param)
            return

        # Commands created by external modules    
        cmd_found = False

        for i in self._modules:
            if i == cmd:
                cmd_found = True

        if not cmd_found:
            # We try to load a module that has the same name as the command
            try:
                importlib.import_module("commands.%s" % cmd)
                line = getattr(sys.modules["commands.%s" % cmd], "run")(param)

                if len(line) > 0:
                    self._send_command(line)

                self._modules.append(cmd)
                    
            except:
                print("Module %s does not exist!" % cmd)

    def _send_command(self, command):
        print(command)
        self._conn.send(command)

    def _quit(self, param):

        if len(param) > 2:
            line = "QUIT :%s" % param[2]
        else:
            line = "QUIT :Don't kill meeeeeeeeeeeeeeeeee"

        self._send_command(line)
        self._conn.disconnect()
        

    def _list(self, to):
        line  = "PRIVMSG %s :Loaded modules: \n" % to

        if len(self._modules) > 0:
            line += '\n'.join(self._modules)
        else:
            line += "No modules have been loaded yet"

        self._send_command(line)
