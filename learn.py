#!/usr/bin/python3

import sys
import random
from pygame import mixer

data_folder = 'data'

def main():
	print()
	mixer.init()

	file_name = sys.argv[1]

	f = open('./'+ data_folder + '/' + file_name + '/' + file_name +'.txt', 'r')
	words = []

	for line in f:
		words.append(line[:-1])

	f.close()


	audio_folder = './'+ data_folder + '/' + file_name + '/audio/'
	while True:
		i = 0
		while i < len(words):
			mixer.music.load(audio_folder + words[i] + '.mp3')
			mixer.music.play()

			while True:
				sys.stdout.write(':>')		
				sys.stdout.flush()
				command = input()
				
				if command == 'r' or command == '':
					mixer.music.play()
				if command == 'n':
					i += 1
					break
				if command == 'b':
					if i == 0:
						break
					else:
						i -= 1
						break
				if command == 'q':
					exit()
		print('Iteration is end')

if __name__ == '__main__':
	main()