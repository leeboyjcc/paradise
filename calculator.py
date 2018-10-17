#!/usr/bin/env python3
import sys

def handle_data(arg):
	arg_list = arg.split(':')
	arg_dict[arg_list[0]] = int(arg_list[1])

def print_data(idno,value):
	print('{}:{:.2f}'.format(idno,value))

def cal_tax(income):
	yincome = income * 0.835 - 3500
	if yincome <= 0:
		tax = 0
	elif yincome <= 1500:
		tax = yincome * 0.03
	elif yincome <= 4500:
		tax = yincome * 0.10 - 105
	elif yincome <= 9000:
		tax = yincome * 0.20 - 555
	elif yincome <= 35000:
		tax = yincome * 0.25 - 1005
	elif yincome <= 55000:
		tax = yincome * 0.30 - 2755
	elif yincome <= 80000:
		tax = yincome * 0.35 - 5505
	else :
		tax = yincome * 0.40 - 13505
	real_income = income * 0.835 - tax
	return real_income
def main():
	for arg in sys.argv[1:]:
		try:
			handle_data(arg)
		except:
			print("Parameter Error")
			sys.exit(1)
	for key,value in arg_dict.items():
		print_data(key,cal_tax(value))
if __name__=='__main__':
	arg_dict={}
	main()
