import sys, os, commands, re, shutil, random

inf = open("./context.scored", 'r')
tokf = open("./namecounts.txt", "r")

if len(sys.argv) != 2:
    print 'script rank_threshold'
    exit(1)

thresh = int(sys.argv[1])

# --- Collect token counts ---

tokcounts = {}

for line in tokf:
    chunks = line.split("\t")
    tokcounts[chunks[0]] = int(chunks[1].rstrip())

tokf.close()

# --- Collect token ranks ---

name = ""
ranks = {}
total = 0

for line in inf:

    line = line.strip()

    if line.startswith("<") :
        if name != "":
            # print name + " -> " + str(ansrank)
            ranks[name] = ansrank
        name = line.lstrip('<').rstrip('>');
        ansrank = -1;
        rank = 0
        total = total + 1
    else :
        rank = rank + 1
        if ansrank == -1 and line.startswith("*") :
            ansrank = rank

ranks[name] = ansrank

print "Number of source tokens : " + str(total)
inf.close()

# --- Compute histogram ---

counts = {}
minc = -1
maxc = -1

for tok in ranks:

    if ranks[tok] > -1 and ranks[tok] < thresh :
        counts[tok] = tokcounts[tok]
        
        if minc == -1 or counts[tok] < minc:
            minc = counts[tok]
        
        if maxc == -1 or counts[tok] > maxc:
            maxc = counts[tok]
    else :
        counts[tok] = 0

print "Min count = " + str(minc) + ", max count " + str(maxc)

minc = 1
maxc = 250000
step = 25000

print "Min count = " + str(minc) + ", max count " + str(maxc) + " step " + str(step)

cutoff = minc
total = 0

while cutoff <= maxc:

    cutnum = 0
 
    for tok in counts:
        if counts[tok] >= cutoff and counts[tok] < (cutoff+step):
            cutnum += 1

    print "[" + str(cutoff) + "," + str(cutoff+step) + ") -> " + str(cutnum)
    total += cutnum

    cutoff += step

print "Total above the threshold " + str(total)
