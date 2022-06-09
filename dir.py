import requests, os

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

dir_list = open("list.txt", "r+")

def clear():
	os.system('cls|clear')

def msgload():
	clear()
	print("""
█▀▄ █ █▀█   █▀▀ █ █▄░█ █▀▄ █▀▀ █▀█
█▄▀ █ █▀▄   █▀░ █ █░▀█ █▄▀ ██▄ █▀▄\n""")
	print("Feito por horizon.sh\n")
	inputs()

def inputs():
	website = input(f"Website:{bcolors.OKGREEN} ")
	loops(website)

def loops(website):
	for lista in dir_list.readlines():
		lista = website + lista.rstrip('\n')
		r = requests.get(lista)
		if r.status_code != 404:
			print(f"{bcolors.OKGREEN} [+] {lista} {bcolors.ENDC}")
try:
	msgload()
except (KeyboardInterrupt):
	print(f"{bcolors.WARNING}\n Voce me fechou :( {bcolors.ENDC}")
except (Exception) as e:
	print(f"{bcolors.FAIL}\n Erro {bcolors.ENDC} \n\n {e}")
