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
            param = [nick, to, "".join(tokens[4:])]
        else:
            param = [nick, to]

        cmd_found = False

        for i in self._modules:
            if i == cmd:
                cmd_found = True

        if not cmd_found:
            # We try to load a module that has the same name as the command
            try:
                importlib.import_module("commands.%s" % cmd)
                x = getattr(sys.modules["commands.%s" % cmd], "run")(param)

                if len(x) > 0:
                    self._conn.send(x)

                self._modules.append(cmd)
                    
            except:
                print("Module %s does not exist!" % cmd)
