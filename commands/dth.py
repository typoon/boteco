from ircmessage import IRCMessage
from connection import Connection

def run(botstate, ircmsg, conn):
    values = []
    hex_val = 0

    if not ircmsg.args:
        return ""

    for i in ircmsg.args:
        try:
            i = i.lstrip("0")
            
            hex_val = hex(int(i,0))
            values.append(str(hex_val))
            
        except:
            invalid = "invalid-%s" % i
            values.append(invalid)

    line = "PRIVMSG %s :%s: %s" % (ircmsg.reply_to, ircmsg.from_nick, " ".join(values))

    conn.send(line)

    return ""

def help():
    help_text = ("DRH: Decimal to Hexadecimal\n"
                 "This command converts a decimal number to hexadecimal.\n"
                 "Use: .dth 30 40 50\n")

    return help_text
