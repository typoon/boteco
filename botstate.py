from channel import Channel

class BotState:

    _instance = None
    _host = ""
    _port = ""
    _nick = ""

    _joined_channels = []
    _loaded_modules  = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BotState, cls).__new__(cls, *args, **kwargs)
        
        return cls._instance

    def joined_channel(self, channel, who):

        # We just joined the channel
        if who == self._nick:
            c = Channel()
            c.users.append(who)
            c.channel = channel
            self._joined_channels.append(c)
        
        for i in self._joined_channels:
            if i.channel == channel:
                i.users.append(who)
            
            
                
