from boteco import Boteco

def parse_conf(file_name):

    with open(file_name, "r") as f:
        for line in f:
            (conf, value) = line.split("=")
            conf = conf.strip()
            value = value.strip()

            if conf == "server":
                global server
                server = value

            elif conf == "port":
                global port
                port = int(value)

            elif conf == "nick":
                global nick
                nick = value

            elif conf == "name":
                global name
                name = value

            elif conf == "channel":
                global channel
                channel = value.split(" ")
        

if __name__ == "__main__":
    # Default values
    server = "irc.freenode.net"
    port = 6667
    nick = "XBoteco"
    name = "XBoteco"
    channel = ["#boteco"]

    file_name = "boteco.cfg"
    parse_conf(file_name)

    print("server = %s" % server)
    print("port = %d" % port)
    print("nick = %s" % nick)
    print("name = %s" % name)
    print("channel = %s" % channel)
    
    
    bot = Boteco(server, port, nick)
    bot.connect()
    bot.join_channel(channel)

    sock = bot.get_socket()

    while bot.is_connected():
        data = sock.read_line()
        print(data)
        bot.parse(data)
