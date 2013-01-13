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

    if not ircmsg.args:
        return ""

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

    line = "PRIVMSG %s :%s: %s" % (ircmsg.reply_to, ircmsg.from_nick, " ".join(values))

    conn.send(line)

    return ""

def help():
    help_text = ("HTD: Hexadecimal to Decimal\n"
                 "This command converts an hexadecimal number to decimal.\n"
                 "It accepts multiple parameters, in three diferent formats\n"
                 "Use: .htd 0x30 30 30h\n")

    return help_text
