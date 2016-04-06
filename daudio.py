#!/usr/bin/python3

import csv
import urllib.request

from selenium import webdriver
from urllib.request import urlretrieve
from pyvirtualdisplay import Display
import time
import os
import sys

def get_audio(word, folder):
	display = Display(visible=0, size=(800, 600))
	display.start()
	browser = webdriver.Firefox()
	url = 'http://www.wordreference.com/enru/' + word
	browser.get(url)

	time.sleep(5) # this is bad
	spisok = ['0', '1', '2', '3', '4']
	for element in spisok:
		try:
			audio = browser.find_element_by_xpath('//audio[@id="aud' + element + '"]/source')
		except Exception:
			return False
		audio_lnk = audio.get_attribute('src')
		if audio_lnk.find('en/uk/London') != -1:
			break 
	
	browser.quit()
	urlretrieve(audio_lnk, folder + word + '.mp3')
	display.stop()
	return True

def main():
	display = Display(visible=0, size=(800, 600))
	display.start()

	folder = sys.argv[1]
	os.mkdir(folder)
	f = open(folder + '.txt', 'r')
	for line in f:
		get_audio(line[:-1], folder)

	f.close()
	display.stop()
	print("All done");


if __name__ == '__main__':
	main()