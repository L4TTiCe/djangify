import os
import re

TEXT = "main/"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def displayPathInfo():
	dirpath = os.getcwd()
	print(bcolors.OKBLUE + "Current Directory is : " + dirpath + bcolors.ENDC)
	foldername = os.path.basename(dirpath)
	print(bcolors.FAIL + "Directory name is : " + foldername + bcolors.ENDC)

def getPath():
	PATH = input(bcolors.HEADER + "\nEnter file name/location : " + bcolors.ENDC)
	return PATH

def checkLine(line):
	words = ['src', 'href', 'url']
	out = list()
	for word in words:
		if line.__contains__(word):
			out.append((True, word))
	if len(out) == 0:
		return None
	else:
		return out

def containsURL(line):
	URL = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
	if re.match(URL, line):
		return True
	else:
		return False

def getIndex(line, word):
	index = line.find(word)
	if word in ['url']:
		start = (index + len(word) + 2)
		quote = line[start - 1]
		if quote not in ['\'', '"']:
			start = (index + len(word) + 1)
			quote = line[start - 1]
			if quote == '(':
				end = line.find(')', start)
			else:
				end = line.find(quote, start)
		else:
			end = line.find(quote, start)
	else:
		start = (index + len(word) + 2)
		quote = line[start - 1]
		end = line.find(quote, start)
	return (start, end)

def djangify(line):
	#print(line)
	if containsURL(line):
		return line
	if line == '#':
		return line
	return " {% static '" + TEXT + line + "' %} "

def processLine(line):
	#line = line.strip()
	instances = checkLine(line)
	#print(line + " " + str(toProcess))
	#print(bcolors.WARNING + line + bcolors.ENDC)

	buffer = line

	if instances:
		for instance in instances:
			index = getIndex(buffer, instance[1])
			out = djangify(buffer[index[0] : index[1]])
			text = buffer[: index[0]] + out + buffer[index[1] :]
			buffer = text
			#if (out != buffer[index[0] : index[1]]):
			#	print(bcolors.WARNING + line + bcolors.ENDC)
			#	print(text)
	
	return buffer

displayPathInfo()
filepath = getPath()

if filepath.__contains__('/'):
	fname = filepath[filepath.rfind('/')+1:]
	extension = filepath[filepath.rfind('.')+1:]
	print(fname + " " + extension)
else:
	fname = filepath
	extension = filepath[filepath.rfind('.')+1:]
	print(fname + " " + extension)

f= open(fname + "_modified." + extension, "w+")

try:
	with open(filepath) as fp:
		line = fp.readline()
		cnt = 1
		while line:
			temp = processLine(line)
			line = fp.readline()
			cnt += 1
			f.write(temp)

except IOError:
    print('An error occurred trying to read the file.')
finally:
	f.close()

print(bcolors.OKGREEN + "Succeeded" + bcolors.ENDC)
