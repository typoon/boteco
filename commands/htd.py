from ircmessage import IRCMessage
from connection import Connection

'''
This module is used to convert a decimal number into and hexadecimal number
Usage:
    .htd 0x21
    .htd 21h
    .htd 47ab
    .htd 0x10 20 30
'''

def run(botstate, ircmsg, conn):
    values = []
    hex_val = 0

    for i in ircmsg.args:
        try:
            if i[0:2] != "0x":
                i = "0x%s" % i

            if i[-1].lower() == 'h':
                i = i[:-1]
            
            hex_val = int(i, 0)
            values.append(str(hex_val))
            
        except:
            invalid = "invalid-%s" % i
            values.append(invalid)

    line = "PRIVMSG %s :%s: %s" % (ircmsg.to, ircmsg.from_nick, " ".join(values))
    print("Module htd: %s\n" % line)

    conn.send(line)

    return ""

def help():
    help_text = ("This commands converts and hexadecimal number to decimal."
                 "It accepts multiple parameters, in three diferent formats"
                 "Use: .htd 0x30 30 30h")

