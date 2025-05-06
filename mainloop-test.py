#!/usr/bin/python3
import argparse
import time

import main_wclasses as initialize


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--worldSize", default=18, help="Specify the length of one side of the world.")
parser.add_argument("-H", "--numHumans", help="Specify the number of human players.")
parser.add_argument("-p", "--numPlayers", help="Specify the number of computer players.")
args = parser.parse_args()

#print(f"{args.worldSize}")


tick = time.perf_counter()    
theWorld = initialize.worldMap(18, 25)#change map spawn details here
theWorld.assemble()

mapData = theWorld.mapData

theWorld.drawMap()
print(f"Recursions: {theWorld.recursions}")
tock = time.perf_counter()
print(f"Time elapsed: {tock - tick:0.4f}")


#print(mapData)

"""
What now?

We need to be assigned to a random city, and
have each COM be assigned to a random city. Probably
should be part of initialize.

Need a city dataset with ID's to do this?

City = [ID, position, (owner?), level, health, wealth,
units inside,]
"""
