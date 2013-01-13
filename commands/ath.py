import binascii

from ircmessage import IRCMessage
from connection import Connection

def run(botstate, ircmsg, conn):
    values = []
    hex_val = ""

    if not ircmsg.args:
        return ""

    i = " ".join(ircmsg.args)
    
    try:
        hex_val = binascii.hexlify(bytes(i,"utf-8"))
        hex_val = "0x%s" % hex_val.decode("utf-8")
        values.append(hex_val)
        
    except:
        invalid = "invalid-%s" % i
        values.append(invalid)

    line = "PRIVMSG %s :%s: %s" % (ircmsg.reply_to, ircmsg.from_nick, " ".join(values))

    conn.send(line)

    return ""

def help():
    help_text = ("ATH: Ascii to Hexadecimal\n"
                 "This command converts an ascii string to hexadecimal.\n"
                 "Use: .ath minha string\n")

    return help_text
