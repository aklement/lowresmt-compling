import sys, os, commands, re, shutil, random

fsrcmap = open("./src.map", 'r')
fcountmap = open("./Number.src.map", 'r')
fscored = open("./context.scored", 'r')
fout = open("./namecounts.txt", "w")

names = []
total = 0

for line in fscored:

    line = line.strip()

    if line.startswith("<") :
        names.append(line.lstrip('<').rstrip('>'))
        total = total + 1

fscored.close()

nameids = {}

for line in fsrcmap:

    chunks = line.split("\t")
    tok = chunks[3].rstrip()

    if tok in names:
        nameids[chunks[0]] = tok

fsrcmap.close()

for line in fcountmap:

    chunks = line.split("\t")
    id = chunks[0]
    
    if id in nameids:
        fout.write(nameids[id] + "\t" + chunks[1].lstrip('[').rstrip(']\n') + "\n")

fscored.close()
fout.close()
