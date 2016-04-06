#!/usr/bin/python3
import pdfkit

res_folder = 'res'
data_folder = 'data'
font_for_trans = 'DejaVu Sans'

def add_tag_b(input_str):
	output_str = '<b>' + input_str + '</b>'
	return output_str

def add_tag_i(input_str):
	output_str = '<i>' + input_str + '</i>'
	return output_str

def add_tag_staff_word(input_str):
	input_str = input_str[1:]
	if input_str[0] == 'I' or input_str[0] == 'V':
		output_str = add_tag_b(input_str)
	else:
		output_str = add_tag_i(input_str)
	return output_str

def add_tag_font(input_str):
	output_str = '<font face="' + font_for_trans + '">'  + input_str + '</font>'
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

def add_tag_div(input_str, in_class):
	output_str = '<div class="' + in_class + '">\n' + input_str + '</div>\n'
	return output_str

def add_tags(input_list):
	for i in range(len(input_list)):
		if i == 0:
			input_list[i] = add_tag_b(input_list[i])
		if i > 0 and input_list[i][0] == '_':
			input_list[i] = add_tag_staff_word(input_list[i])
		if i > 0 and input_list[i][0] == '[' and input_list[i][-1] == ']': #if our word is transcription
			input_list[i] = add_tag_font(input_list[i])
		if i > 0 and is_dec(input_list[i][0]) and (input_list[i][-1] == '>' or input_list[i][-1] == '.'):
			input_list[i] = add_tag_for_dec(input_list[i])
	return input_list


def gen_html(words):

	input_file = open('./' + res_folder + '/mueller7GPLunicode.txt', 'r')
	buff = input_file.readlines()
	input_file.close()
	res_strngs = []

	for s_word in words:
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
			if s_word == buff_list_str[0]:
				buff_list_str.remove('')
				# print(buff_list_str)
				buff_list_str = add_tags(buff_list_str)
				res_strngs.append(' '.join(buff_list_str))
				break
			if i == len(buff) - 1:
				print('Cлово НЕ найдено: ' + s_word)
	
	itr = 0
	for i in range(len(res_strngs)):
		res_strngs[i] = add_tag_div(res_strngs[i], 'word')
		#разделение на блоки по 5 слов
		itr += 1
		if itr == 1:
			res_strngs[i] = '<div class="block">\n' + res_strngs[i]
		if itr == 5 or i == len(res_strngs) - 1:
			res_strngs[i] = res_strngs[i] + '</div>\n\n'
			itr = 0

	templ = open('./' + res_folder + '/templ.html', 'r')
	out_html = templ.read()
	templ.close()
	
	out_html = out_html.replace('#words#','\n'.join(res_strngs))

	return out_html

def gen_html_f(words, file_name):
	out_html = gen_html(words)
	out_html_patch = './' + data_folder + '/'+ file_name + '/' + file_name + '.html'
	out_html_f = open(out_html_patch, 'w')
	out_html_f.write(out_html)
	out_html_f.close()

def gen_pdf_f(words, file_name):
	
	html = gen_html(words)
	html = html.replace('margin-left: 350px;', 'margin-left: 20px;')

	out_pdf_patch = './' + data_folder + '/'+ file_name + '/' + file_name + '.pdf'
	pdfkit.from_string(html, out_pdf_patch)

def main():
	print("Hello World")


if __name__ == '__main__':
	main()