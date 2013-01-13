import os
import imp
import importlib
import sys

from connection import Connection
from ircmessage import IRCMessage
from botstate   import BotState

class BotCommands:

    _modules = []

    def __init__(self):
        self._conn = Connection()
        self.botstate = BotState()
        self.load_modules()

    def load_modules(self):
        for _, _, files in os.walk("./commands"):
            for f in files:
                path, ext = os.path.splitext(f)
                if path == "__init__":
                    continue
                    
                if ext == ".py":
                    try:
                        mod_name = "commands.%s" % path
                        mod = importlib.import_module(mod_name)
                        self._modules.append(mod)
                    except:
                        print("Cannot load module %s (%s)" % (f, sys.exc_info()))

    def execute(self, ircmsg):
        # Pre-defined commands
        if ircmsg.cmd == "list":
            self._list_modules(ircmsg)
            return

        elif ircmsg.cmd == "quit":
            self._quit(ircmsg)
            return

        elif ircmsg.cmd == "reload":
            self._reload_modules(ircmsg)
            return

        elif ircmsg.cmd == "join" or ircmsg.cmd == "j":
            self._join(ircmsg)
            return

        elif ircmsg.cmd == "channels":
            self._list_channels(ircmsg)
            return

        elif ircmsg.cmd == "help" or ircmsg.cmd == "h":
            self._help(ircmsg)
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
                line = getattr(sys.modules[mod_name], "run")(self.botstate, ircmsg, self._conn)

                print("Loaded module %s\n" % mod_name)

                if len(line) > 0:
                    self.send_command(line)

                self._modules.append(mod)
                    
            except:
                msg = "Module %s does not exist or has errors (%s)" % (ircmsg.cmd, sys.exc_info())
                self.send_message(ircmsg.reply_to, msg)
                
        else:
            line = getattr(sys.modules[mod_name], "run")(self.botstate, ircmsg, self._conn)
            
            if len(line) > 0:
                    self.send_command(line)



    def send_command(self, line):
        self._conn.send(line)

    def send_message(self, to, msg):
        line = "PRIVMSG %s :%s" % (to, msg)
        self.send_command(line)

    def join(self, channel):
        ircmsg = IRCMessage("")

        ircmsg.msg_type = "JOIN"
        ircmsg.cmd = "join"
        ircmsg.args = channel

        self._join(ircmsg)

    def _read_line(self):
        return self._conn.read_line()

    def _list_modules(self, ircmsg):
        line  = "Loaded modules: "

        if len(self._modules) > 0:
            loaded_modules = [m.__name__[m.__name__.find(".")+1:] for m in self._modules]
            line += ", ".join(loaded_modules)
        else:
            line  = "No modules have been loaded yet"

        self.send_message(ircmsg.reply_to, line)

    def _quit(self, ircmsg):

        if not ircmsg.args:
            line = "QUIT :%s" % " ".join(ircmsg.args)
        else:
            line = "QUIT :Don't kill meeeeeeeeeeeeeeeeee"

        self.send_command(line)
        self._conn.disconnect()

    def _reload_modules(self, ircmsg):
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
                    self.send_message(ircmsg.reply_to, msg)
        else:
            self.load_modules()  # Loads any new modules that have been created
            
            for i in self._modules:
                try:
                    imp.reload(i)
                    name = i.__name__
                    reloaded_modules.append(name[name.find(".")+1:]) # Remove commands. from the module name
                except:
                    msg = "Module %s cannot be reloaded (%s)" % (i.__name__, sys.exc_info())
                    self.send_message(ircmsg.reply_to, msg)

        if len(reloaded_modules) > 0:
            msg = "The following modules were reloaded: %s" % " ".join(reloaded_modules)
        else:
            msg = "No modules have been reloaded"
            
        self.send_message(ircmsg.reply_to, msg)

    def _join(self, ircmsg):
        
        if not ircmsg.args:
            return

        for i in ircmsg.args:
            line = "JOIN %s" % i
            self.send_command(line)

    def _list_channels(self, ircmsg):
        state = self.botstate
        channels = []

        for i in state._joined_channels:
            channels.append(i.channel)

        msg = "In channels: %s" % " ".join(channels)
        self.send_message(ircmsg.reply_to, msg)

    def _help(self, ircmsg):
        if not ircmsg.args:
            return

        cmd = ircmsg.args[0]

        if cmd in [m.__name__[m.__name__.find(".")+1:] for m in self._modules]:
            mod_name = "commands.%s" % cmd
            help_text = getattr(sys.modules[mod_name], "help")()

            for l in help_text.split("\n"):
                self.send_message(ircmsg.from_nick, l)
