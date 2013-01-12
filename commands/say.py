from ircmessage import IRCMessage
from connection import Connection

'''
This module is used to make the Bot repeat whatever you want him to
Usage:
    .say Hello World
'''

def run(ircmsg, conn):

    if ircmsg.args == "":
        return ""

    channel = ircmsg.args[0]
    if channel[0] != "#":
        channel = ircmsg.to
        line = "PRIVMSG %s :%s" % (channel, " ".join(ircmsg.args))
    else:
        line = "PRIVMSG %s :%s" % (channel, " ".join(ircmsg.args[1:]))
    
    return line
