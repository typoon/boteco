from ircmessage import IRCMessage
from connection import Connection

'''
This module is used to make the Bot repeat whatever you want him to
Usage:
    .say Hello World
'''

def run(ircmsg, conn):
    return "PRIVMSG %s :%s" % (ircmsg.to, " ".join(ircmsg.args))
