#http://bled.scbikes.com/api/stations/public-list?format=json

import requests
import sys
import json



cena = [[0,5,8,9], [5,0,3,7], [8,3,0,9], [9,7,9,0]]

# cene bodo kasneje pridobljene prek api klicev in bodo predstavljale trenutno situacijo na cesti

API_id = "44b0468e"
API_key = "a0857c7529197f3f92fde4ef9f0a4b48"

capacity = 2
maxcapacity = 2


def dex(vektor):
    return vektor.index(min(vektor))

def preveri(vektor):
    for i in vektor:
        if i < 0:
            return False
    return True



def izberi(vektor, poz):
    global capacity
    global maxcapacity
    global cena
    index = -1

    if capacity == 0:
        min = 10

        for i in range(0, len(vektor)):

            if cena[poz][i] < min and poz != i and vektor[i] > 0:
                index = i
                min = cena[poz][i]

    elif capacity == maxcapacity:
        min = 10

        for i in range(0, len(vektor)):

            if cena[poz][i] < min and poz != i and vektor[i] < 0:
                index = i
                min = cena[poz][i]
    else:
        min = 10

        for i in range(0, len(vektor)):

            if cena[poz][i] < min and poz != i:
                index = i
                min = cena[poz][i]


    return index

def plusminus(postaje, avg):
    vektor = []
    for x in postaje:
        if x > avg :
            vektor.append(avg  - x)
        elif x < avg:
            vektor.append(avg -x)
        else:
            vektor.append(0)

    return vektor

def pot(vektor, zaporedje, poz):
    global odgovor
    global capacity
    global API_id
    global API_key
    global maxcapacity
    global counter


    if preveri(vektor) == True:
        return zaporedje


    if poz < 0:
        poz = dex(vektor)

    if vektor[poz] < 0 and capacity > 0:

        mini = min(abs(vektor[poz]), capacity)
        capacity -= mini
        vektor[poz] += mini
        zaporedje.append(odgovor[poz]["name"]+" "+str(mini)+"+ ")

    elif vektor[poz] > 0 and capacity < maxcapacity:

        mini = min(abs(vektor[poz]), (maxcapacity - capacity ))
        capacity += mini
        vektor[poz] -= mini
        zaporedje.append(odgovor[poz]["name"]+" "+str(mini)+"- ")

    poz = izberi(vektor, poz)

    if poz == -1:
        return zaporedje

    return pot(vektor, zaporedje,poz)



odgovor = requests.get("http://bled.scbikes.com/api/stations/public-list?format=json").json()


list = []
sum = 0
for num in odgovor:

    naVoljo = num["numberOfFreeBikes"] - num["numberOfTotalFaulty"]
    list.append(naVoljo)
    sum += naVoljo

avg = sum // len(list)


print(plusminus(list, avg))
print(list)
vek = plusminus(list, avg)
print(pot(vek,[], -1))
print(vek)
