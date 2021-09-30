from random import randint
import string
import random

def randomsix():
    num = '0966118'
    for x in range(4):
        value = randint(0, 9)
        num = num + str(value)
    print(num)    

for x in range(10): 
    randomsix()


def generateEmail():
    byom = "@byom.de"
    for x in range(3):
        randomLetter = chr(random.randint(ord('a'), ord('z')))
        byom = randomLetter + byom
    print(byom)

generateEmail()    