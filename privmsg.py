import config
import commands

def parse(self, recv):
    irc_user_nick = recv.split ( '!' ) [ 0 ] . split ( ":")[1]
    irc_user_host = recv.split ( '@' ) [ 1 ] . split ( ' ' ) [ 0 ]
    irc_user_message = self.data_to_message(recv)
    chan = recv.split()[2]  #channel
    
    print ( ( "[%s] %s: %s" ) % (self.irc_host, irc_user_nick, irc_user_message) )
    # Message starts with command prefix?
    if ( irc_user_message != '' ):
        if ( irc_user_message[0] == config.prefix ):
            self.command = irc_user_message[1:].replace("'","''")
            commands.parse(self, irc_user_nick, chan)
