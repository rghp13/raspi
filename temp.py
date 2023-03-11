from sense_hat import SenseHat
from coloraide import Color
import re
sense = SenseHat()

hot = Color("red")
cold = Color("blue")
temp = sense.get_temperature()
temp = int(temp)
i = Color("blue").steps("red", steps=40)
color = i[temp].to_string()
p = re.compile(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)')
rgb = [float(x) for x in p.findall(color)]
rgb2 = [int(rgb) for rgb in rgb]
temp = str(temp)
sense.show_message(temp, scroll_speed=0.25, text_colour=rgb2, back_colour=[0, 255, 0])
sense.clear()
