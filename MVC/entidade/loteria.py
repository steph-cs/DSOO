from entidade.aposta import Aposta
from entidade.jogo import Jogo
from entidade.sorteio import Sorteio

class Loteria():
    def __init__(self):
        self.__apostas = []
        self.__sorteios = []
        print('Loteria criada!')

    def add_aposta(self, aposta):
        if isinstance(aposta, Aposta) and aposta not in self.__apostas and len(aposta.apostadores())>0:
            self.__apostas.append(aposta)
            print('Aposta adicionada!')
        else:
            print('Verifique a aposta!')

    def del_aposta(self, aposta):
        if isinstance(aposta, Aposta) and aposta in self.__apostas:
            self.__apostas.remove(aposta)

    def apostas(self):
        return self.__apostas

    def apostas_por_jogo(self, jogo):
        if isinstance(jogo, Jogo):
            apostas = []
            for aposta in self.__apostas:
                if aposta.jogo == jogo:
                    apostas.append(aposta)
            return apostas

    def apostas_por_data(self, dia, mes, ano):
        apostas = []
        for aposta in self.__apostas:
            if (aposta.dia == dia) and (aposta.mes == mes) and (aposta.ano == ano):
                apostas.append(aposta)
        return apostas

    def apostas_por_jogo_data(self, jogo, dia, mes, ano):
        apostas_jogo_data = []
        apostas_jogo = self.apostas_por_jogo(jogo)
        apostas_data = self.apostas_por_data(dia, mes, ano)
        for ap_jogo in apostas_jogo:
            for ap_dat in apostas_data:
                if ap_jogo == ap_dat:
                    apostas_jogo_data.append(ap_jogo)
        return apostas_jogo_data

    def add_sorteio(self, sorteio):
        if isinstance(sorteio, Sorteio) and sorteio not in self.__sorteios:
            self.__sorteios.append(sorteio)

    def del_sorteio(self, sorteio):
        if isinstance(sorteio, Sorteio) and sorteio in self.__sorteios:
            self.__sorteios.remove(sorteio)

    def sorteios(self):
        return self.__sorteios

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

    def ganhadores_por_jogo(self, jogo):
        apostas = []
        apostas_jogo = self.apostas_por_jogo(jogo)
        apostas_ganhas = self.apostas_ganhas()
        for ap_ganha in apostas_ganhas:
            for ap_jogo in apostas_jogo:
                if ap_ganha == ap_jogo:
                    apostas.append(ap_ganha)
        return apostas

    def ganhadores_por_data_jogo(self, dia, mes, ano, jogo = None):
        apostas_ganhas = self.apostas_ganhas()
        apostas = []
        apostas_data = self.apostas_por_data(dia,mes,ano)
        if jogo is None:
            apostas_ganhas = self.apostas_ganhas()
            for ap_ganha in apostas_ganhas:
                for ap_data in apostas_data:
                    if ap_data == ap_ganha:
                        apostas.append(ap_ganha)
        else:
            apostas_jogo = self.ganhadores_por_jogo(jogo)
            for ap_jogo in apostas_jogo:
                for ap_data in apostas_data:
                    if ap_jogo == ap_data:
                        apostas.append(ap_jogo)
        return apostas

    def ultimas_apostas_ganhas(self, qnt, jogo = None ):
        if jogo is None:
            apostas = self.apostas_ganhas()[-qnt:]
        else:
            apostas = self.ganhadores_por_jogo(jogo)[-qnt]
        return apostas

    def sorteio_numeros_recorrentes(self, jogo):
        # qnt de numeros recorrentes de acordo com a qnt minima de numeros do jogo
        apostas = self.ganhadores_por_jogo(jogo)
        qnt_num = jogo.min_numeros
        numeros = {}
        for aposta in apostas:
            for numero in aposta.numeros:
                if numero in numeros:
                    numeros[numero] = (numeros[numero] + 1)
                else: 
                    numeros[numero] = 1

        return (sorted(numeros.items(), key= lambda x: x[1],reverse= True))[:qnt_num]



    
