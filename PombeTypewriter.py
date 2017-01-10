#Welcome to PombeTypewriter!
#This scripts takes a text input (and some other parameters) and produces a csv file that can be read by the RoTor with Stinger attachment.
#The target plate will be in 1536 format

#Your text goes here, one list entry per line of text. The script will warn you if a line is too long. See the preview for more.
text= ['YEAH',
        'Dave',
      'hello']

sourceFormat = 96#96 or 384
toUse = ['A1', 'A2']#Specify the positions with colonies to use
betweenLetters = 1#Space between letters
betweenWords = 3#Space between words
betweenLines = 2#space between lines


###The code starts here###

from matplotlib import pyplot as plt
import numpy as np
from random import choice

#Letter code, credit to https://gist.github.com/woodworker/7696835
letters = {
    "A":[
        "1111",
        "1001",
        "1111",
        "1001"
    ],
    "B": [
        "1000",
        "1110",
        "1010",
        "1110"
    ],
    "C": [
        "1111",
        "1000",
        "1000",
        "1111"
    ],
    "D": [
        "1110",
        "1001",
        "1001",
        "1110"
    ],
    "E": [
        "1111",
        "1110",
        "1000",
        "1110"
    ],
    "F": [
        "1111",
        "1110",
        "1000",
        "1000"
    ],
    "G": [
        "1111",
        "1000",
        "1001",
        "1111"
    ],
    "H": [
        "1000",
        "1000",
        "1110",
        "1001"
    ],
    "I": [
        "1",
        "1",
        "1",
        "1"
    ],
    "J": [
        "01",
        "01",
        "01",
        "11"
    ],
    "K": [
        "1010",
        "1100",
        "1010",
        "1001"
    ],
    "L": [
        "1000",
        "1000",
        "1000",
        "1111"
    ],
    "M": [
        "10001",
        "11011",
        "10101",
        "10001"
    ],
    "N": [
        "1001",
        "1101",
        "1011",
        "1001"
    ],
    "O": [
        "1111",
        "1001",
        "1001",
        "1111"
    ],
    "P": [
        "1110",
        "1001",
        "1110",
        "1000"
    ],
    "Q": [
        "11110",
        "10010",
        "11110",
        "00001"
    ],
    "R": [
        "1110",
        "1001",
        "1110",
        "1010"
    ],
    "S": [
        "1111",
        "1000",
        "1001",
        "1111"
    ],
    "T": [
        "1111",
        "0100",
        "0100",
        "0100"
    ],
    "U": [
        "1001",
        "1001",
        "1001",
        "1111"
    ],
    "V": [
        "1000001",
        "0100010",
        "0010100",
        "0001000"
    ],
    "W": [
        "10001",
        "10001",
        "10101",
        "01110"
    ],
    "X": [
        "01010",
        "00100",
        "01010",
        "10001"
    ],
    "Y": [
        "10001",
        "01010",
        "00100",
        "00100"
    ],
    "Z": [
        "1111",
        "0010",
        "0100",
        "0100"
    ],
    " ": [
        "  ",
        "  ",
        "  ",
        "  "
    ]
}

assert len(text) < 4, 'Too many lines in text. There can only be up to three lines.'
assert sourceFormat in [96, 384], 'Source format has to be 96 or 384. Do not put quotes around the number.'
for pos in toUse:
    assert isinstance(pos, basestring), 'toUse position invalid. Put quotes around each position.'
assert isinstance(betweenLines, int), 'betweenLines invalid. Do not put quotes around the number.'
assert isinstance(betweenWords, int), 'betweenWords invalid. Do not put quotes around the number.'
assert isinstance(betweenLetters, int), 'betweenLetters invalid. Do not put quotes around the number.'

#typesetting
#First hack the char dict a bit
letters['betweenChars'] = ['0' * betweenLetters]*4
letters[' '] = ['0' * betweenWords]*4
for key in letters.keys():
    outStrMat = []
    for row in letters[key]:
        outStrMat.append([int(char) for char in list(row)])
    letters[key] = np.array(outStrMat)

#Put together a big matrix with 1 in positions where a colony should be
lineMaster = []
for line in [textline.upper() for textline in text]:
    lineSlave = []
    for l in line:
        lineSlave.append(letters[l])
        lineSlave.append(letters['betweenChars'])
    wholeLine = np.hstack(lineSlave)
    assert wholeLine.shape[1] < 49, 'One of the lines is too long.'
    wholeLine = np.hstack((wholeLine, [[0] * (48-wholeLine.shape[1])]*4 ))
    assert wholeLine.shape == (4,48)
    lineMaster.append(wholeLine)
    for i in range(betweenLines):
        lineMaster.append([[0] * 48])
lineMaster = np.vstack(lineMaster)
assert lineMaster.shape[0] < 33, 'Too many rows or two much space between rows.'
lineMaster = np.vstack((lineMaster, [[0] * 48]*(32-lineMaster.shape[0])))
assert lineMaster.shape == (32,48)

#preview
plt.imshow(lineMaster, cmap='hot', interpolation='nearest')
plt.xticks(())
plt.yticks(())
plt.savefig('preview.png')
plt.clf()

#write Stinger file
rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 
        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF']
assert len(rows)==32
with open('stinger_file.csv', 'w') as oF:
    oF.write('SOURCEPLATEID,SOURCEDENSITY,SOURCECOLONYCOLUMN,SOURCECOLONYROW,TARGETPLATEID,TARGETDENSITY,TARGETCOLONYCOLUMN,TARGETCOLONYROW\n')
    for row in range(32):
        for col in range(48):
            if lineMaster[row,col] == 1:
                sourcePos = choice(toUse)
                params = (sourceFormat, sourcePos[0], sourcePos[1:], rows[row], col)
                oF.write('Source 1,%i,%s,%s,Target 1,1536,%s,%i\n'%params)
