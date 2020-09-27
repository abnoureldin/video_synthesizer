import pyaudio
import sys
import numpy as np
import aubio
import pygame
import random
from threading import Thread
import queue
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-input",required=False, type=int, help="Audio Input Device")
parser.add_argument("-f", action="store_true", help="Run in Fullscreen Mode")
args = parser.parse_args()

if not args.input:
	print("No input device specified. Printing list of input devices:")
	p = pyaudio.PyAudio()
	for i in range(p.get_device_count()):
		print("Device number (%i): %s" % (i,p.get_device_info_by_index(i)\
			.get("name")))
	print("Run this program with -input 1, or the number of desired input.")
	exit()

pygame.init()

if args.f:
	screenWidth, screenHeight = 1024, 768
	screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN | pygame.HWSURF | pygame.DOUBLEBUF)

else:
	screenWidth, screenHeight = 800, 800
	screen = pygame.display.set_mode((screenWidth, screenHeight))


white = (255,255,255)
black = (0,0,0)

class Circle(object):
	def __init__(self, x,y, colour, size):
		self.x = x
		self.y = y
		self.colour = colour
		self.size = size

	def shrink(self):
		self.size -= 3

colours = [(229, 244, 227), (93, 169, 233), (0, 63, 145), (255, 255, 255), (109, 50, 109)]
circleList = []

p = pyaudio.PyAudio()
clock = pygame.time.Clock()

buffer_size = 4096
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100

stream = p.open(format=pyaudio_format,
				channels=n_channels,
				rate=samplerate,
				input=True,
				input_device_index=args.input,
				frames_per_buffer=buffer_size)

time.sleep(1)

tolerance = 0.8
win_s = 4096
hop_s = buffer_size // 2
onset = aubio.onset("default", win_s, hop_s, samplerate)

q = queue.Queue()

def draw():
	running = True
	while running:
		key = pygame.key.get_pressed()

		if key[pygame.K_q]:
			running = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		if not q.empty():
			b = q.get()
			newCircle = Circle(random.randint(0, screenWidth), random.randint(0, screenHeight),
				random.choice(colours), 700)
			circleList.append(newCircle)

		screen.fill(black)
		for place, circle in enumerate(circleList):
			if circle.size < 1:
				circleList.pop(place)
			else:
				pygame.draw.circle(screen, circle.colour, (circle.x,circle.y), circle.size)
			circle.shrink()

			pygame.display.flip()
			clock.tick(90)















