import os
from connection import Connection
from privatemessageparser import PrivateMessageParser

class Boteco:

    joined_channels = []

    def __init__(self, host, port, nick):
        self.host = host
        self.port = port
        self.nick = nick
        
        self._is_connected = False
        self._privmsg_parser = PrivateMessageParser()

    def connect(self):
        if self._is_connected:
            return

        self._sock = Connection()
        self._sock.connect(self.host, self.port)
        
        while 1:
            data = self._read_line()
            if data == "":
                break
                
            print(data)

        self._send_command("NICK " + self.nick)
        self._send_command("USER " + self.nick + " myhost myhost :" + self.nick)

        # Read the whole MOTD and whatever else there is and simply ignore
        while 1:
            data = self._read_line()
            if data == "":
                return
                
            print(data)

    def join_channel(self, channel):
        self._send_command("JOIN "+ channel)
      
    def is_connected(self):
        return self._sock.is_connected

    def parse(self):
            
        data = self._read_line()
       
        if len(data) == 0:
            return

        print("Parse: %s" % data)

        tokens = [el.strip() for el in data.split(" ")]

        if len(tokens) < 2:
            return;

        # This is probably a PING or ERROR command
        if len(tokens) == 2:
            if tokens[0] == "PING":
                self._send_command("PONG " + tokens[1])

            elif tokens[0] == "ERROR":
                self._sock.disconnect()

            else:
                print(tokens)

        # Everything else I guess
        if len(tokens) >= 3:
            if tokens[1] == "PRIVMSG":
                self._handle_privmsg(data)

            if tokens[1] == "JOIN":
                self._handle_join(data)


    def _read_line(self):
        return self._sock.read_line()

    def _send_command(self, command):
        print(command)
        self._sock.send(command)

    def _handle_privmsg(self, data):
        self._privmsg_parser.parse(data)
        

    def _handle_join(self, data):
        tokens = [el.strip() for el in data.split(" ")]

        people_on_channel = []
        joined_channel = tokens[2]

        while 1:
            data = self._read_line()
            print(data)
            tokens = [el.strip() for el in data.split(" ")]

            if tokens[1] == "353":
                for i in tokens[5:]:
                    people_on_channel.append(i.strip(":"))
                
            elif tokens[1] == "366":
                # End of names, we are done reading data
                break

            else:
                break

        print("Joined channel %s" % joined_channel)
        for i in people_on_channel:
            print("Person %s is on channel" % i)

        print("End of JOIN")
        
