import imp
import importlib
import commands
import sys
from ircmessage import IRCMessage
from connection import Connection

class PrivateMessageParser:

    _modules = []
    
    def __init__(self):
        self._conn = Connection()

    def parse(self, data):
        ircmsg = IRCMessage(data)

        if ircmsg.cmd == "":
            print("No command : %s " % data)
            return

        # Pre-defined commands
        if ircmsg.cmd == "list":
            self._list(ircmsg)
            return

        elif ircmsg.cmd == "quit":
            self._quit(ircmsg)
            return

        elif ircmsg.cmd == "reload":
            self._reload(ircmsg)
            return

        # Commands created by external modules
        mod_name = "commands.%s" % ircmsg.cmd
        cmd_found = False
        
        for i in self._modules:
            if i.__name__ == mod_name:
                cmd_found = True

        if not cmd_found:
            # We try to load a module that has the same name as the command
            try:
                
                mod = importlib.import_module(mod_name)
                line = getattr(sys.modules[mod_name], "run")(ircmsg, self._conn)

                print("Loaded module %s\n" % mod_name)

                if len(line) > 0:
                    self._send_command(line)

                self._modules.append(mod)
                    
            except:
                msg = "Module %s does not exist or has errors (%s)" % (ircmsg.cmd, sys.exc_info())
                self._send_message(ircmsg, msg)
                
        else:
            line = getattr(sys.modules[mod_name], "run")(ircmsg, self._conn)
            
            if len(line) > 0:
                    self._send_command(line)
            
    def _send_command(self, line):
        self._conn.send(line)

    def _send_message(self, ircmsg, msg):
        line = "PRIVMSG %s :%s" % (ircmsg.to, msg)
        self._send_command(line)

    def _quit(self, ircmsg):

        if ircmsg.args != "":
            line = "QUIT :%s" % " ".join(ircmsg.args)
        else:
            line = "QUIT :Don't kill meeeeeeeeeeeeeeeeee"

        self._send_command(line)
        self._conn.disconnect()
        

    def _list(self, ircmsg):
        line  = "Loaded modules: "

        if len(self._modules) > 0:
            loaded_modules = [m.__name__ for m in self._modules]
            line += ", ".join(loaded_modules)
        else:
            line  = "No modules have been loaded yet"

        self._send_message(ircmsg, line)

    def _reload(self, ircmsg):
        '''
        Reloads specified module. If no module is specified, reload them all
        If module specified has not been loaded yet, load it
        '''

        reloaded_modules = []
        module_found = False

        if len(ircmsg.args) > 0:
            for i in ircmsg.args:
                mod_name = "commands.%s" % i
                
                try:
                    for j in self._modules:
                        if mod_name == j.__name__:
                            imp.reload(j)
                            reloaded_modules.append(i)
                            module_found = True

                    if module_found == False:
                        mod = importlib.import_module(mod_name)
                        reloaded_modules.append(i)
                        self._modules.append(mod)
                        
                except:
                    msg = "Module %s cannot be reloaded (%s)" % (i, sys.exc_info())
                    self._send_message(ircmsg, msg)
        else:
            for i in self._modules:
                try:
                    imp.reload(i)
                    name = i.__name__
                    reloaded_modules.append(name[name.find(".")+1:]) # Remove commands. from the module name
                except:
                    msg = "Module %s cannot be reloaded (%s)" % (i.__name__, sys.exc_info())
                    self._send_message(ircmsg, msg)

        if len(reloaded_modules) > 0:
            msg = "The following modules were reloaded: %s" % " ".join(reloaded_modules)
        else:
            msg = "No modules have been reloaded"
            
        self._send_message(ircmsg, msg)
