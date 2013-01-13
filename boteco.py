import os
import imp
import importlib
import commands
import sys

from connection  import Connection
from botstate    import BotState
from botcommands import BotCommands
from ircmessage  import IRCMessage

class Boteco:

    def __init__(self, host, port, nick):
        self.state = BotState()
        self.state._host = host
        self.state._port = port
        self.state._nick = nick
        
        self._command = BotCommands()
        self._is_connected = False

    def connect(self):
        if self._is_connected:
            return

        self._sock = Connection()
        self._sock.connect(self.state._host, self.state._port)
        
        while 1:
            data = self._read_line()
            if data == "":
                break
                
            print(data)

        self._send_command("NICK " + self.state._nick)
        self._send_command("USER " + self.state._nick + " myhost myhost :" + self.state._nick)

        # Read the whole MOTD and whatever else there is and simply ignore
        while 1:
            data = self._read_line()
            if data == "":
                return
                
            print(data)

    def get_socket(self):
        return self._sock

    def join_channel(self, channel):
        self._command.join(channel)
      
    def is_connected(self):
        return self._sock.is_connected

    def parse(self, data):
        ircmsg = IRCMessage(data)

        if ircmsg.msg_type == "":
            return

        if ircmsg.msg_type == "PING":
            self._send_command("PONG " + ircmsg.from_host)
            
        elif ircmsg.msg_type == "ERROR":
            self._sock.disconnect()

        elif ircmsg.msg_type == "JOIN":
            self._handle_join(ircmsg)

        elif ircmsg.msg_type == "PRIVMSG":
            self._handle_privmsg(ircmsg)


    def _read_line(self):
        return self._sock.read_line()

    def _send_command(self, command):
        self._command.send_command(command)

    def _send_message(self, ircmsg, msg):
        self._command.send_message(ircmsg, msg)

    def _handle_privmsg(self, ircmsg):
        if ircmsg.cmd == "":
            return

        self._command.execute(ircmsg)

    # TODO: Might want to rewrite this...
    def _handle_join(self, ircmsg):

        # Is it the bot joining?
        if ircmsg.from_nick == self.state._nick:
            people_on_channel = []
            joined_channel = ircmsg.to
            
            while 1:
                data = self._read_line()
                print(data)
                
                tokens = [el.strip() for el in data.split(" ")]

                if tokens[1] == "353":
                    for i in tokens[5:]:
                        people_on_channel.append(i.strip(":"))
                        self.state.joined_channel(ircmsg.to, i.strip(":"))

                        print("Joined channel %s\n" % ircmsg.to)
                    
                elif tokens[1] == "366":
                    # End of names, we are done reading data
                    break


            print("Joined channel %s" % joined_channel)
            for i in people_on_channel:
                print("Person %s is on channel" % i)

            print("End of JOIN")
    
        else:
            self.state.joined_channel(ircmsg.to, ircmsg.from_nick)
