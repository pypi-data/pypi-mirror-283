from time import sleep
import asyncio, os, sys, time, logging,json,random
from datetime import datetime


b = "\033[1;34m"
c = "\033[1;36m"
d = "\033[0m"
h = "\033[1;32m"
k = "\033[1;33m"
m = "\033[1;31m"
p = "\033[1;37m"
u = "\033[1;35m"
mm = "\033[101m\033[1;31m"
mp = "\033[101m\033[1;37m"
hp = "\033[1;7m"
n = "\n"

def Ascii_calvin(strings,versi):
	acssi = {"a" : ["┌─┐","├─┤","┴ ┴"],"b":["┌┐ ","├┴┐","└─┘"],"c":["┌─┐","│  ","└─┘"],"d":["┌┬┐"," ││","─┴┘"],"e":["┌─┐","├┤ ","└─┘"],"f" : ["┌─┐","├┤ ","└  "],"g":["┌─┐","│ ┬","└─┘"],"h":["┬ ┬","├─┤","┴ ┴"],"i":["┬","│","┴"],"j":[" ┬"," │","└┘"],"k":["┬┌─","├┴┐","┴ ┴"],"l" : ["┬  ","│  ","┴─┘"],"m":["┌┬┐","│││","┴ ┴"],"n":["┌┐┌","│││","┘└┘"],"o":["┌─┐","│ │","└─┘"],"p":["┌─┐","├─┘","┴  "],"q" : ["┌─┐ ","│─┼┐","└─┘└"],"r":["┬─┐","├┬┘","┴└─"],"s":["┌─┐","└─┐","└─┘"],"t":["┌┬┐"," │ "," ┴ "],"u":["┬ ┬","│ │","└─┘"],"v" : ["┬  ┬","└┐┌┘"," └┘ "],"w":["┬ ┬","│││","└┴┘"],"x":["─┐ ┬","┌┴┬┘","┴ └─"],"y":["┬ ┬","└┬┘"," ┴ "],"z":["┌─┐","┌─┘","└─┘"]}
	string = list(strings)
	for i in string:
		print(b+acssi[i][0],flush=True,end="")
	print(k+" versi "+m+": "+h+versi)
	for i in string:
		print(c+acssi[i][1],flush=True,end="")
	print(k+" status"+m+": "+h+"on")
	for i in string:
		print(p+acssi[i][2],flush=True,end="")
	print(n,flush=True,end="")

def banner(title,versi):
	os.system('cls' if os.name=='nt' else 'clear')
	print(p+"─"*16+m+"> "+h+"Scrypt by "+p+"iewil"+m+" <"+p+"─"*15)
	Ascii_calvin(title,versi)
	line()
	print(mm+"["+mp+"▶"+mm+"]"+d,flush=True,end="")
	print(p+" https://www.youtube.com/c/iewil")
	print(hp+" >_"+d,flush=True,end="")
	print(b+" Team-Function-INDO")
	line()
	print(mm+"["+mp+"!"+mm+"]"+d,flush=True,end="")
	print(m+" SCRIPT GRATIS TIDAK UNTUK DI OBRAL!"+b)
	line()

def line():
	print(b+"─"*50)

def echo(message,eror = False):
	#print(m+"["+p+f'{datetime.now().strftime("%H:%M:%S")}'+m+"] ",flush=True,end="")
	if eror:
		print(m+"["+p+"!"+m+"]"+p+message)
	else:
		print(h+"["+p+"√"+h+"]"+p+message)

def simpan(filename):
	if os.path.exists(filename):
		data = open(filename).read()
	else:
		print(k+"["+p+"+"+k+"]"+p+"Input "+filename+p+" : \n")
		data = input()
		file = open(filename,"w")
		file.write(data)
		file.close()
	return data

def auth(wr):
	nic = []
	nic.append(wr + " i" + p + "ewil-official")
	nic.append(wr + " ie" + p + "wil-official")
	nic.append(wr + " iew" + p + "il-official")
	nic.append(" i" + wr + "ewi" + p + "l-official")
	nic.append(" ie" + wr + "wil" + p + "-official")
	nic.append(" iew" + wr + "il-" + p + "official")
	nic.append(" iewi" + wr + "l-o" + p + "fficial")
	nic.append(" iewil" + wr + "-of" + p + "ficial")
	nic.append(" iewil" + wr + "-of" + p + "ficial")
	nic.append(" iewil-" + wr + "off" + p + "icial")
	nic.append(" iewil-o" + wr + "ffi" + p + "cial")
	nic.append(" iewil-of" + wr + "fic" + p + "ial")
	nic.append(" iewil-of" + wr + "fic" + p + "ial")
	nic.append(" iewil-off" + wr + "ici" + p + "al")
	nic.append(" iewil-offi" + wr + "cia" + p + "l")
	nic.append(p + " iewil-offic" + wr + "ial")
	nic.append(p + " iewil-offici" + wr + "al")
	nic.append(p + " iewil-officia" + wr + "l")
	return nic

def timer(tmr):
	col = [b, c, d, h, k, m, u]
	sym = [' ─ ', ' / ', ' │ ', ' \ ']
	timr = time.time() + tmr
	a = 0
	while True:
		a += 1
		x = random.choice(col)
		nic = auth(x)
		res = timr - time.time()
		if res < 1:
			break
		print("         " + x + sym[a % 4] + p + str(int(res / 3600)) + x + ":" + p + str(int((res % 3600) / 60)) + x + ":" + p + str(int(res % 60)) + nic[a % 18], end="\r")
		time.sleep(0.1)

def explode(str, rsc):
	return rsc.split(str)