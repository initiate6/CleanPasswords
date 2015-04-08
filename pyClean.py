#!/usr/bin/env python2.7
#Python 2.7.x
#Name: pyClean.py
#By: INIT_6
#Cleans large dictionaries removing configured chars via regex.
#For more information check out my blog: https://blog.init6.me/?p=63
##
#    pyClean is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 of the License.
#
#    pyClean is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    To receive a copy of the GNU General Public License
#    see <http://www.gnu.org/licenses/>.
##

import sys
import re
import time
import getopt
import multiprocessing as mp
import Queue

def usage():
	print(''' 
--help        Prints this help
--file        File containing words you want to clean up. 1 word per line
--threads     Number of processors
--output      Output filename. Default: input file name plus .out
--lines       Lines per chuck to read Default [10000]
--startRegex  Regex to remove at start of line. Default [^[\d|\W]+]
--endRegex    Regex to remove at end of line.   Default [[\d|\W]+$]
	''')

def read_in_chunks(file_object, chunk_size):
    while True:
        data = file_object.readlines(chunk_size)
        if not data:
            break
        yield data

def cleanIt(piece, sRegex, eRegex, outFile):
	#clean up words list ^regex and $regex to remove special chars and numbers as soon as it hits a char done.
	# ^[\d|\W]+
	# [\d|\W]+$
	wordList = []
	for line in piece:
		temp = re.sub(sRegex,'',line)  #Remove regex at start of line. 
		if temp:
			out = re.sub(eRegex,'',temp) #If removed at start of line now lets remove at end of line.
		else:
			out = re.sub(eRegex,'',line) #if we didn't remove anything at start of line lets try to remove at end.
			
		wordList.append(out)

		if out == None and temp == None: #if no regex matches append line.
			wordList.append(line)
			print("out: %s\ntemp: %s\nline: %s") % (out, temp, line)

	#Makes sure this piece/chunk doesn't contain dup words and is greater than 3char and write chunk to file.
    	final = []
	wordList.sort()
	temp = ""
	for item in wordList:
        	if item != temp:
			if len(item) > 3:
				final.append(item)
				temp = item

	#Open file in append mode and write list
	with open(outFile, 'a') as f:
		for word in final:
			f.write(word+'\n')	

def eat_queue(job_queue, result_queue, sRegex, eRegex, outFile):
	#Eats input queue, feeds output queue
	proc_name = mp.current_process().name
	while True:
	    piece = job_queue.get()
	    if piece is None:
		print(proc_name + " DONE")
		break
	    else:
		result_queue.put(cleanIt(piece, sRegex, eRegex, outFile ))
	result_queue.put(None)

def put_tasks(job_queue, f, lines, threads):
	#Feeds the job queue
	for piece in read_in_chunks(f, lines):
		job_queue.put(piece)

	for _ in range(threads):
		job_queue.put(None)

def run(f, threads, outFile, lines, sRegex, eRegex):
	job_queue = mp.Queue(maxsize=10*threads)
	result_queue = mp.Queue()

	workers_list = []

	#A process for feeding job queue with the input file
	task_gen = mp.Process(target=put_tasks, name="task_gen", args=(job_queue, f, lines, threads))

	workers_list.append(task_gen)

	for i in range(threads):
		tmp = mp.Process(target=eat_queue, name="w%d" % (i+1), args=(job_queue, result_queue, sRegex, eRegex, outFile))
		workers_list.append(tmp)

	for worker in workers_list:
		print("Start worker %s") % worker
		worker.start()

	count = 0
	while count < threads:
		if result_queue.get() is None:
			count += 1

	for worker in workers_list:
		worker.join()
		print("worker %s finished!") % worker.name 


def main(argv):
	#initialize list here instead of moving stuff out of main() 
	(inFile, threads, outFile, lines, startRegex, endRegex) = (None, None, None, None, None, None)

	try:
		opts, args = getopt.getopt(argv, "Hf:olset", ["Help", "file=", "threads=", "output=", "lines=", "startRegex=", "endRegex="])

	except:
		usage()
		sys.exit(1)

	for opt, arg in opts:
		if opt in ("-H", "--help"):
			usage()
			sys.exit()
		elif opt in ("-f", "--file"):
			inFile = arg
		elif opt in ("-t", "--threads"):
			threads = arg
		elif opt in ("-o", "--output"):
			outFile = arg
		elif opt in ("-l", "--lines"):
			lines = int(arg)
		elif opt in ("-s", "--startRegex"):
			startRegex = arg
		elif opt in ("-e", "--endRegex"):
			endRegex = arg

	if inFile:
		f = open(inFile)
	else:
		print("\nOops, Forgot to included file to read.\n")
		usage()
		sys.exit(1)		

	#Set defaults if not set on command line. 
	try:
		if not outFile:
			outFile = str(inFile) + ".out"
		if not lines:
			lines = 10000
		if not startRegex:
			startRegex = '^[\d|\W]+'
		if not endRegex:
			endRegex = '[\d|\W]+$'
		if not threads:
			threads = mp.cpu_count()

	except Exception as e:
		print("Error when trying to set default values: %s") % e

	#Compile regex before Generator to save CPU/MEM for doing it each time.
	try:
		sRegex = re.compile(startRegex)
		eRegex = re.compile(endRegex)

	except Exception as e:
		print("Error when trying to set regex compile: %s") % e

	print("Running with config: Input File: %s, Threads: %s, Lines: %s, startRegex: %s, endRegex: %s\n") % (inFile, threads, outFile, lines, sRegex, eRegex)
	run(f, threads, outFile, lines, sRegex, eRegex)
	

if __name__ == "__main__":
	print('''
pyClean.py by INIT_6
Cleans large dictionaries removing configured chars via regex.
For more information check out my blog: https://blog.init6.me/?p=63\n
	''')
	main(sys.argv[1:])
