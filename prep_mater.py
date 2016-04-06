#!/usr/bin/python3
import daudio
import genpdf
import sys
from os import mkdir
from shutil import move

data_folder = 'data'

def main():
	try:
		file_name = sys.argv[1]
	except IndexError:
		print('\nДля того чтобы выйти, введите \'q\'\nВы не ввели имя файла, откуда нужно считать слова\nПожалуйста, введите имя файла.')
		sys.stdout.write(':>')		
		sys.stdout.flush()
		file_name = input()
		if file_name == 'q':
			exit()
	while True:
		try:
			f = open('./' + file_name, 'r')
		except FileNotFoundError:
			print('Такой файл не найден')
			sys.stdout.write(':>')		
			sys.stdout.flush()
			file_name = input()
			if file_name == 'q':
				exit()
		else:
			break

	words = []
	for line in f:
		words.append(line[:-1])
	f.close()
	mkdir('./'+ data_folder + '/' + file_name[:-4])
	mkdir('./'+ data_folder + '/' + file_name[:-4] + '/audio')
	move(file_name, './' + data_folder + '/' + file_name[:-4] + '/' + file_name)
	file_name = file_name[:-4]
	

	genpdf.gen_html_f(words, file_name)
	print('HTML файл сгенерирован')
	genpdf.gen_pdf_f(words, file_name)
	print('PDF файл сгенерирован')

	audio_folder = './'+ data_folder + '/' + file_name + '/audio/'
	print('Началась загрузка аудоматерила...')
	for word in words:
		if not daudio.get_audio(word, audio_folder):
			print("Аудио НЕ загружено: " + word)
	print('Аудиоматериал загружен')
	print('Все сделано, Мой Господин!')


if __name__ == '__main__':
	main()