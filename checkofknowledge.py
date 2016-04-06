#!/usr/bin/python3

import sys
import random
import time
from pygame import mixer
from colorama import Fore, Style

data_folder = 'data'

def main():

	mixer.init()

	words = []
	print(Fore.GREEN + 'Приветсвую тебя, Мой Господин!')
	print(Style.RESET_ALL)

	file_name = sys.argv[1]

	f = open('./'+ data_folder + '/' + file_name + '/' + file_name +'.txt', 'r')

	for line in f:
		words.append(line[:-1])
	
	f.close()
	random.shuffle(words)

	audio_folder = './'+ data_folder + '/' + file_name + '/audio/'

	while True:
		for word in words:
			mixer.music.load(audio_folder + word + '.mp3')
			mixer.music.play()

			while True:
				sys.stdout.write(':>')		
				sys.stdout.flush()
				inputWord = input()

				if inputWord == word:
					print(Fore.GREEN + 'RIGHT')
					print(Style.RESET_ALL)
					break

				if inputWord != word and inputWord != 'r' and inputWord != 'q' and inputWord != 'n' and inputWord != '':
					print(Fore.RED + 'WRONG')
					print(Style.RESET_ALL)
					print(word + '\n')
					mixer.music.play()
					time.sleep(2)
					break

				if inputWord == 'r' or inputWord == '':
					mixer.music.play()

				if inputWord == 'n':
					break

				if inputWord == 'q':
					exit()
		print('Iteration is end')
		random.shuffle(words)



if __name__ == '__main__':
	main()