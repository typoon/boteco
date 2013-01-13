from ircmessage import IRCMessage
from connection import Connection

'''
This module is used to make the Bot repeat whatever you want him to
Usage:
    .say #channel Hello World
    .say Hello World
'''

def run(botstate, ircmsg, conn):

    if not ircmsg.args:
        return ""

    channel = ircmsg.args[0]
    if channel[0] != "#":
        channel = ircmsg.reply_to
        line = "PRIVMSG %s :%s" % (channel, " ".join(ircmsg.args))
    else:
        line = "PRIVMSG %s :%s" % (channel, " ".join(ircmsg.args[1:]))
    
    return line

def help():
    help_text = ("SAY: I talk for you\n"
                 "This module is used to make the Bot repeat whatever you want him to\n"
                 "Usage:\n"
                 "  .say #channel Hello World\n"
                 "  .say Hello World\n")

    return help_text
