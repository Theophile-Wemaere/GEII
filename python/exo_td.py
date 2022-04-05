#!/usr/bin/python3

voy = ['a','e','i','o','u','y','A','E','I','O','U','Y']

def get_voy(string):
    count=0
    for i in range(len(string)):
        for j in range(len(voy)):
            if string[i]==voy[j]:
                count+=1
    return count;

def get_wo_voy(string):
    word_wo_voy=""
    for i in string:
        if i not in voy:
            word_wo_voy += i
    return word_wo_voy

prenom = input("quelle est votre prénom ? : ")
nom = input("quelle est votre nom ? : ")

all = prenom + " " + nom

nb_letters = len(prenom) + len(nom)
nb_voy = get_voy(all)
word_wo = get_wo_voy(all)

print(all + " contient " + str(nb_letters) + " lettres dont " + str(nb_voy) + " voyelles")
print("mot sans voyelles : " + word_wo)
