import sys
import re
import time
import getopt


def writeIt(wordList, outFile):
	#Open file in append mode and write list
	with open(outFile, 'a') as f:
		for word in wordList:
			f.write(word+'\n')

#def read_in_chunks(file_object, chunk_size=1073741824):
def read_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.readlines(chunk_size)
        if not data:
            break
        yield data

#get uniq out of the string list
def uniq(listobj):
    final = []
    listobj.sort()
    temp = ""
    for item in listobj:
        if item != temp:
            if len(item) > 3:
                final.append(item)
                temp = item  
    return final

def cleanIt(piece):
	#clean up words list ^regex and $regex to remove special chars and numbers as soon as it hits a char done.
	# ^[\d|\W]+
	# [\d|\W]+$
	wordList = []
	for line in piece:
		temp = re.sub('^[\d|\W]+','',line)
		if temp:
			out = re.sub('[\d|\W]+$','',temp)
		else:
			out = re.sub('[\d|\W]+$','',line)
	
		wordList.append(out)
	return wordList

def usage():
	print(''' 
		--help Prints help
		--file File containing
		--output output to file
		--lines How many lines per chuck
		''')
def main(argv):
	try:
		opts, args = getopt.getopt(argv, "Hf:o:l:", ["Help", "file=", "output=", "lines="])

	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-H", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--file"):
			inFile = arg
		elif opt in ("-o", "--output"):
			outFile = arg
		elif opt in ("-l", "--lines"):
			lines = int(arg)

	f = open(inFile)
	for piece in read_in_chunks(f, lines):
		wordList = cleanIt(piece)
		writeIt( uniq(wordList), outFile )

if __name__ == "__main__":
	main(sys.argv[1:])
