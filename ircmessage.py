class IRCMessage:
    from_host = ""
    from_nick = ""
    msg_type  = ""  # PRIVMSG, NOTICE, etc..
    to = ""
    msg = ""       # The whole message, including the !cmd in case it is present
    cmd = ""       # The !cmd or .cmd without the leading char "." or "!"
    args = ""      # The whole message without the !cmd and represented as list
                   # created by spliting the message on spaces
                   # msg.split(" ")

    def __init__(self, data):
        self.populate(data)

    def populate(self, data):

        if len(data) <= 0:
            return
        
        tokens = [el.strip() for el in data.split(" ")]

        if len(tokens) == 2:
            if tokens[0] == "PING":
                self._populate_ping(data)

            elif tokens[0] == "ERROR":
                self._populate_error(data)

        elif len(tokens) >= 3:
            if tokens[1] == "PRIVMSG":
                self._populate_privmsg(data)

            elif tokens[1] == "JOIN":
                self._populate_join(data)

    def _populate_ping(self, data):
        tokens = [el.strip() for el in data.split(" ")]

        self.from_host = tokens[1]
        self.msg_type = "PING"

    def _populate_error(self, data):
        self.msg_type = "ERROR"

    def _populate_privmsg(self, data):
        # Example data
        # :Gilgamesh!~gilgamesh@some_ip PRIVMSG #gilgabot :cool story bro
        
        data = data.strip()
        tokens = [el.strip() for el in data.split(" ")]

        self.from_nick = data[1:data.find("!")]
        self.from_host = data[data.find("!")+1:data.find(" ")]
        self.msg_type  = "PRIVMSG"
        self.to        = tokens[2]
        self.msg       = (" ".join(tokens[3:])).lstrip(":").strip()

        if self.msg[0] == "." or self.msg[0] == "!":
            if self.msg.find(" ") > 0:
                self.cmd  = self.msg[1:self.msg.find(" ")]
                self.args = self.msg[self.msg.find(" ")+1:].split(" ")
            else:
                self.cmd  = self.msg[1:]
                self.args = ""

    def _populate_join(self, data):
        # Example data
        # :Boteco!~Boteco@186.214.63.85 JOIN #boteco

        data = data.strip()
        tokens = [el.strip() for el in data.split(" ")]

        self.from_nick = data[1:data.find("!")]
        self.from_host = data[data.find("!")+1:data.find(" ")]
        self.msg_type  = "JOIN"
        self.to        = tokens[2]
