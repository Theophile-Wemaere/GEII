#!/usr/bin/python3
from random import randrange
import os

def count_char(file):
    count=0
    countl=0
    f = open(file,'r')
    for line in f:
        countl+=1
        for i in range(len(line)):
            if line[i]!=" ":
                count+=1
    print(count)
    print(countl)
    
def count_byte(file):
    file_size = os.path.getsize(file)
    print("File Size is :", file_size, "bytes")
    f = open(file,'rb')
    f.seek(0,2) # move the cursor to the end of the file
    size = f.tell()
    print("File Size is :", size, "bytes")
    
    
def to_cpp(file):
    f = open(file,'r')
    cert="const uint8_t serverCertFingerprint[] = {0x"
    line=f.readline()
    pos=line.index(":")
    hexa=line[:pos]
    cert+=hexa
    line=line[pos+1:]
    for i in range(18):
        pos=line.index(":")
        hexa=line[:pos]
        cert+=",0x"+hexa
        line=line[pos+1:]
    print(cert+",0x"+line+"};")
    
def test():
    f=open('cert.txt','r')
    cert="const uint8_t serverCertFingerprint[] = {"
    line=f.readline()
    out=line.split(':')
    for i in out:
        cert+="0x"
        cert+=i+","
    print(cert[:-1]+"};")
    
def removeChar():
    first=['un','deux','trois','quatre','cinq']
    second=['deux','cinq']
    out=[]
    for i in first:
        if i not in second:
            out+=[i]
    else:
        pass
    print(out)
            
def count_word(file):
    count=0
    f=open(file,'r')
    data=f.read()
    lines = data.split()
    count+=len(lines)
    print(count)


def remove_punct(word):
    nw=""
    punct=[',',';',':','!','?','.','/','*','\"','\'','-','_']
    
    for i in word[::-1]:
        if i not in punct:
            nw=word
            break
        else:
            word=word[:-1]
           
    print(nw)
            

if __name__ == '__main__':
    print("hello word")
