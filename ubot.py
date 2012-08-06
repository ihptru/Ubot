#!/usr/bin/env python
import socket
import time
import re
import multiprocessing

import config
import list_players
import privmsg

class IRC_Bot:

    def __init__(self):
        self.irc_host = config.host
        self.irc_port = config.port
        self.irc_nick = config.nick
        self.channels = config.channels
        self.command = ""
        
        self.irc_sock = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
        
        self.listen_return = ''

    def __del__(self):
        self.irc_sock.close()
        
    def connect(self):
        while 1:
            try:
                self.irc_sock.connect ((self.irc_host, self.irc_port))
                break
            except:
                print ("Error: Could not connect to IRC; Host: " + str(self.irc_host) + "Port: " + str(self.irc_port))
                time.sleep(60)
                continue
     
        multiprocessing.Process(target=list_players.start, args=(self,)).start()
        
        print ("Connected to: " + str(self.irc_host) + ":" + str(self.irc_port))
        
        def bot_connect(self):
            str_buff = ("NICK %s \r\n") % (self.irc_nick)
            self.irc_sock.send (str_buff.encode())
            print (("[%s] Setting bot nick to " + str(self.irc_nick)) % (self.irc_host))

            str_buff = ("USER %s 8 * :X\r\n") % (self.irc_nick)
            self.irc_sock.send (str_buff.encode())
            print (("[%s] Setting User") % (self.irc_host))

            for channel in self.channels:
                str_buff = ( "JOIN %s \r\n" ) % (channel)
                self.irc_sock.send (str_buff.encode())
                print (("[%s] Joining channel " + channel) % (self.irc_host))
        bot_connect(self)
        
        while 1:
            if self.listen():
                if ( self.listen_return == 'Nick in Use' ):
                    self.irc_nick = self.irc_nick + "_"
                    bot_connect(self)
                    continue

    def listen(self):
        while 1:
            recv = self.irc_sock.recv( 4096 )
            recv = self.decode_stream( recv )

            data = self.handle_recv( recv )
            for recv in data:
                if recv.find ( "PING" ) != -1:
                    self.irc_sock.send ( ("PONG "+ recv.split() [ 1 ] + "\r\n").encode() )

                if recv.find ( " PRIVMSG " ) != -1:
                    privmsg.parse(self, recv)

                if recv.find ( " 433 * "+self.irc_nick+" " ) != -1:
                    print(("[%s] Nick is already in use!!!") % (self.irc_host))
                    self.listen_return = 'Nick in Use'
                    return True
                
                if recv.find ( " 471 " ) != -1:
                    if ( recv.split()[1] == "471" ):
                        channel = recv.split()[3]
                        print (("[%s] "+channel+" is full!") % (self.irc_host))

                if recv.find ( " 473 " ) != -1:
                    if ( recv.split()[1] == "473" ):
                        channel = recv.split()[3]
                        print (("[%s] "+channel+" is invite only!") % (self.irc_host))

                if recv.find ( " 474 " ) != -1:
                    if ( recv.split()[1] == "474" ):
                        channel = recv.split()[3]
                        print (("[%s] Bot is banned from "+channel+" !") % (self.irc_host))

                if recv.find ( " 475 " ) != -1:
                    if ( recv.split()[1] == "475" ):
                        channel = recv.split()[3]
                        print (("[%s] Key is required for "+channel+" !") % (self.irc_host))

    def data_to_message(self, data):
        data = data[data.find(" :")+2:]
        return data

    #handle as single line request as multiple ( split recv into pieces before processing it )
    def handle_recv(self, recv):
        regex = re.compile('(.*?)\r\n')
        recv = regex.findall(recv)
        return recv

    # helper to remove some insanity.
    def send_reply(self, data, user, channel):
        target = channel if channel.startswith('#') else user
        self.send_message_to_channel(data,target)

    #another helper
    def decode_stream(self, stream):
        try:
            return stream.decode("utf-8")
        except:
            return stream.decode("CP1252")

    # This function sends a message to a channel or user
    def send_message_to_channel(self, data, channel):
        print ( ( "[%s] %s: %s") % (self.irc_host, self.irc_nick, data) )
        self.irc_sock.send( (("PRIVMSG %s :%s\r\n") % (channel, data[0:512])).encode() )

    def send_notice(self, data, user):
        print ( ( "[%s] NOTICE to %s: %s" ) % (self.irc_host, user, data) )
        str_buff = ( "NOTICE %s :%s\r\n" ) % (user,data)
        self.irc_sock.send (str_buff.encode())

    def send_names(self, channel):
        str_buff = ( "NAMES %s \r\n" ) % (channel)
        self.irc_sock.send (str_buff.encode())

bot = IRC_Bot()
bot.connect()
