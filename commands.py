import urllib2
import re

def parse(self, user, channel):
    command = (self.command).split()
    if command[0] == "uplayers":
        if len(command) == 1:
            try:
                url = 'http://ix.lv-vl.net:5000'
                stream = urllib2.urlopen(url).read().decode()

                names =[]
                try:
                    temp_names = stream.split("<p>")[1:]
                    for temp in temp_names:
                        names.append(re.findall("<font size=5px>(.*)</font>.*", temp)[0])
                except:
                    names = []
                if len(names) == 0:
                    self.send_message_to_channel("No one seems to be in-game", channel)
                else:
                    seconds = re.findall("data is (.*) seconds", stream)
                    self.send_message_to_channel(("Data is "+seconds[0]+" seconds old: "+" | ".join(names)).rstrip(" | "), channel)
            except Exception as e:
                print(str(e))
