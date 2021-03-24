'''
#a ={'a':5, 'b':2, 'c':3,'d':7, 'e':1}
#print((sorted(a.items(), key = lambda x : x[1], reverse= True))[:3])
#[('d', 7), ('a', 5), ('c', 3)]


import time
from datetime import date, timedelta

today = date(2021,3,15)
data_sorteio = date(2021,4,10)
#  data hj (20/03/2021)
#  data sorteio (domingo)
print("Faltam: {} dias para o sorteio ".format((abs(today - data_sorteio)).days) )


if today.weekday() == 6:
    #retorna o resultado do sorteio
    pass
else:
    qnt = 6 - today.weekday()
    print(today + timedelta(days= qnt))
    print((today + timedelta(days= qnt)).strftime("%d/%m/%y"))

   
def pega_dados(dados: list):
    infos = {}
    for dado in dados:
        infos[dado] = (input("{}: ".format(dado)))
    return infos

a = pega_dados(['nome','numeros'])
a['numeros'] = a['numeros'].split(',')
for info in a.values():
    print(info)
    print(type(info))

def apostas_ganhas(self):
        apostas = []
        for aposta in self.__apostas:
            cont = 0
            for sorteio in self.__sorteios:
                if (aposta.jogo == sorteio.jogo) and (aposta.mes == sorteio.mes) and (sorteio.dia - 7 <=aposta.dia<=sorteio.dia):
                    for numero in sorteio.numeros:
                        if numero in aposta.numeros:
                            cont += 1
                    if cont == len(sorteio.numeros):
                        apostas.append(aposta)
        return apostas
'''

