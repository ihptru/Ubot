import urllib2
import time
import re

def start(self):
    while 1:
        try:
            url = 'http://ix.lv-vl.net:5000'
            initial_stream = urllib2.urlopen(url).read().decode()

            initial_names =[]
            try:
                temp_names = initial_stream.split("<p>")[1:]
                for temp in temp_names:
                    initial_names.append(re.findall("<font size=5px>(.*)</font>.*", temp)[0])
            except:
                initial_names = []

            while 1:
                time.sleep(30)
                stream = urllib2.urlopen(url).read().decode()
                
                names =[]
                try:
                    temp_names = stream.split("<p>")[1:]
                    for temp in temp_names:
                        names.append(re.findall("<font size=5px>(.*)</font>.*", temp)[0])
                except:
                    names = []
                
                for name in names:
                    if name not in initial_names:
                        seconds = re.findall("data is (.*) seconds", stream)
                        self.send_message_to_channel(name.strip()+" has been detected in-game! (data is "+seconds[0]+" seconds old)", "#Untitled.ctf")
            
                initial_names = []
                for name in names:
                    initial_names.append(name)
        except:
            time.sleep(60)
            continue
