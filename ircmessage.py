class IRCMessage:
    from_host = ""
    from_nick = ""
    msg_type = ""  # PRIVMSG, NOTICE, etc..
    to = ""
    msg = ""       # The whole message, including the !cmd in case it is present
    cmd = ""       # The !cmd or .cmd without the leading char "." or "!"
    args = ""      # The whole message without the !cmd and represented as list
                   # created by spliting the message on spaces
                   # msg.split(" ")

    def __init__(self, data):
        self.populate(data)

    def populate(self, data):
        tokens = [el.strip() for el in data.split(" ")]

        if tokens[1] == "PRIVMSG":
            self._populate_privmsg(data);

    def _populate_privmsg(self, data):
        # Example data
        # :Gilgamesh!~gilgamesh@some_ip PRIVMSG #gilgabot :cool story bro
        
        data = data.strip()
        tokens = [el.strip() for el in data.split(" ")]

        self.from_nick = data[1:data.find("!")]
        self.from_host = data[data.find("!")+1:data.find(" ")]
        self.msg_type  = "PRIVMSG"
        self.to        = tokens[2]
        self.msg       = (" ".join(tokens[3:])).lstrip(":")

        if self.msg[0] == "." or self.msg[0] == "!":
            if self.msg.find(" ") > 0:
                self.cmd  = self.msg[1:self.msg.find(" ")]
                self.args = self.msg[self.msg.find(" ")+1:].split(" ")
            else:
                self.cmd  = self.msg[1:]
                self.args = ""
