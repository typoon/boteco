from ircmessage import IRCMessage
from connection import Connection

'''
This module makes the bot join a channel
Usage:
    .join #channel1 #channel2 #channel3
    .join #channel
'''

def run(ircmsg, conn):

    if ircmsg.args == "":
        return ""

    for i in ircmsg.args:
        line = "JOIN %s" % i
        conn.send(line)

    return ""
