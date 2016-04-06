#!/usr/bin/python3
import sys
import daudio
import os.path
from pygame import mixer

res_folder = 'res'
audio_cash_folder = './acash/'


def add_tag_inv(input_str):
	output_str = '\033[7m' + input_str + '\033[0m'
	return output_str

def add_tag_b(input_str):
	output_str = '\033[1m' + input_str + '\033[0m'
	return output_str

def add_tag_i(input_str):
	output_str = '\033[3m' + input_str + '\033[0m'
	return output_str

def add_tag_staff_word(input_str):
	input_str = input_str[1:]
	if input_str[0] == 'I' or input_str[0] == 'V':
		output_str = add_tag_b(input_str)
	else:
		output_str = add_tag_i(input_str)
	return output_str


def add_tag_for_dec(input_str):
	dec_dig = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
	rom_dec = ['I', 'II', 'III', 'VI', 'V', 'VI', 'VII', 'VIII', 'IX']
	if input_str[-1] == '>':
		input_str = input_str[:-1] + '.'
		output_str = add_tag_b(input_str)
	else:
		for i in range(len(dec_dig)):
			if dec_dig[i] == input_str[0]:
				output_str = input_str.replace(dec_dig[i], rom_dec[i])
				output_str = add_tag_b(output_str)
				return output_str
				

	return output_str

def is_dec(input_char):
	dec_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	for ch in dec_chars:
		if input_char == ch:
			return True
	return False

def add_tags(input_list):
	for i in range(len(input_list)):
		if i == 0:
			input_list[i] = add_tag_inv(input_list[i])
		if i > 0 and input_list[i][0] == '_':
			input_list[i] = add_tag_staff_word(input_list[i])
		if i > 0 and input_list[i][0] == '[' and input_list[i][-1] == ']': #if our word is transcription
			input_list[i] = add_tag_b(input_list[i])
		if i > 0 and is_dec(input_list[i][0]) and (input_list[i][-1] == '>' or input_list[i][-1] == '.'):
			input_list[i] = add_tag_for_dec(input_list[i])
	return input_list



def print_color_green(text):
	print('\033[32m' + text + '\033[0m')

def print_color_red(text):
	print('\033[31m' + text + '\033[0m')


def main():

	input_file = open('./' + res_folder + '/mueller7GPLunicode.txt', 'r')
	buff = input_file.readlines()
	input_file.close()

	print_color_green('Добро пожаловать в интерактивный словарь \nВ. Мюллера 7 издание\n')
	print_color_green('Для того чтобы выйти из словаря введите \'q\'\n')

	mixer.init()

	while True:
		sys.stdout.write(':>')		
		sys.stdout.flush()
		word = input()
		if word == 'q':
			exit()
		if word == '':
			continue

		res_str = ''

		for i in range(len(buff)):
			buff_list_str = buff[i].split(' ')
			# print(buff_list_str)
			if buff_list_str[1] != '':
				ind_empty = buff_list_str.index('')
				buf_word_l = []
				for j in range(ind_empty):
					buf_word_l.append(buff_list_str[j])
				for j in buf_word_l:
					buff_list_str.remove(j)
				buff_list_str.insert(0, ' '.join(buf_word_l))
			if word == buff_list_str[0]:
				buff_list_str.remove('')
				# print(buff_list_str)
				res_str = add_tags(buff_list_str)
				print(' '.join(res_str))
				if(not os.path.isfile(audio_cash_folder + word + '.mp3')):
					daudio.get_audio(word, audio_cash_folder)
				try:
					mixer.music.load(audio_cash_folder + word + '.mp3')
				except:
					print_color_red('Нет аудио файла для воспроизведения')
				else:
					mixer.music.play()

				break
			if i == len(buff) - 1:
				print_color_red('Cлово в словаре не найдено')


    # print('\033[36mCYANCOLOR\033[0m')



if __name__ == '__main__':
	main()