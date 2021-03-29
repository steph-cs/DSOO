from entidade.aposta import Aposta
from entidade.jogo import Jogo
from entidade.sorteio import Sorteio
from datetime import date, timedelta
from entidade.exception import QuantidadeNumerosIncorreta, NaoExiste, JaExiste, ListaVazia

class Loteria():
    def __init__(self):
        self.__apostas = []
        self.__sorteios = []

    def add_aposta(self, aposta):
        if isinstance(aposta, Aposta) and aposta not in self.__apostas:
            if len(aposta.apostadores())>0:
                self.__apostas.append(aposta)
            else:
                raise NaoExiste('apostadores')
        else:
            raise JaExiste('aposta')

    def del_aposta(self, aposta):
        if isinstance(aposta, Aposta) and aposta in self.__apostas:
            self.__apostas.remove(aposta)
        else:
            raise NaoExiste('aposta')

    def apostas(self):
        return self.__apostas

    def apostas_por_jogo(self, jogo):
        if isinstance(jogo, Jogo):
            apostas = []
            for aposta in self.__apostas:
                if aposta.jogo == jogo:
                    apostas.append(aposta)
            return apostas

    def apostas_por_data(self, data):
        apostas = []
        for aposta in self.__apostas:
            if aposta.data == data:
                apostas.append(aposta)
        return apostas

    def apostas_por_jogo_data(self, jogo, data):
        apostas_jogo_data = []
        apostas_jogo = self.apostas_por_jogo(jogo)
        apostas_data = self.apostas_por_data(data)
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
                if (aposta.jogo == sorteio.jogo) and (sorteio.data - timedelta(days=7)<=aposta.data<= sorteio.data):
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

    def ganhadores_por_data_jogo(self, data, jogo = None):
        apostas_ganhas = self.apostas_ganhas()
        apostas = []
        apostas_data = self.apostas_por_data(data)
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
        if len(self.__apostas)>=1:
            if jogo is None:
                apostas = self.apostas_ganhas()[-qnt:]
            else:
                apostas = self.ganhadores_por_jogo(jogo)[-qnt]
            return apostas
        else:
            raise ListaVazia('apostas ganhas')

    def sorteio_numeros_recorrentes(self, jogo):
        # numeros que mais foram apostados dentre as apostas ganhas
        # qnt de numeros recorrentes de acordo com a qnt minima de numeros do jogo
        apostas = self.ganhadores_por_jogo(jogo)
        if apostas >= 1:
            qnt_num = jogo.min_numeros
            numeros = {}
            for aposta in apostas:
                for numero in aposta.numeros:
                    if numero in numeros:
                        numeros[numero] = (numeros[numero] + 1)
                    else: 
                        numeros[numero] = 1

            return (sorted(numeros.items(), key= lambda x: x[1],reverse = True))[:qnt_num]
        else:
            raise ListaVazia('apostas ganhas')



    
