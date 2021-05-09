from entidade.aposta import Aposta
from entidade.jogo import Jogo
from entidade.sorteio import Sorteio
from datetime import date, timedelta
from entidade.exception import QuantidadeNumerosIncorreta, NaoExiste, JaExiste, ListaVazia

class Loteria():
    __instance = None

    def __init__(self):
        self.__apostas = []
        self.__sorteios = []

    def __new__(cls, *args, **kwargs):
        if Loteria.__instance is None:
            Loteria.__instance = object.__new__(cls)
        return Loteria.__instance

#acoes aposta
    def add_aposta(self, aposta: Aposta):
        if isinstance(aposta, Aposta) and aposta not in self.__apostas:
            if len(aposta.apostadores())>0:
                self.__apostas.append(aposta)
            else:
                raise NaoExiste('apostadores')
        else:
            raise JaExiste('aposta')

    def del_aposta(self, aposta: Aposta):
        if isinstance(aposta, Aposta) and aposta in self.__apostas:
            self.__apostas.remove(aposta)
        else:
            raise NaoExiste('aposta')

    def apostas(self):
        return sorted(self.__apostas , key= lambda x : x.data)

    def apostas_por_jogo(self, jogo: Jogo):
        if isinstance(jogo, Jogo):
            apostas = []
            for aposta in self.apostas():
                if aposta.jogo.nome == jogo.nome:
                    apostas.append(aposta)
            if len(apostas) >= 1:
                return apostas
            else:
                raise ListaVazia('apostas por jogo')

    def apostas_por_data(self, data_min: date, data_max: date):
        apostas = []
        for aposta in self.apostas():
            if  data_min<= aposta.data <= data_max:
                apostas.append(aposta)
        if len(apostas) >= 1:
            return apostas
        else:
            raise ListaVazia('apostas por data')

    def apostas_por_jogo_data(self, jogo: Jogo,  data_min: date, data_max: date):
        apostas_jogo_data = []
        apostas_jogo = self.apostas_por_jogo(jogo)
        apostas_data = self.apostas_por_data( data_min, data_max)
        for ap_jogo in apostas_jogo:
            for ap_dat in apostas_data:
                if ap_jogo == ap_dat:
                    apostas_jogo_data.append(ap_jogo)
        if len(apostas_jogo_data) >= 1:
            return apostas_jogo_data
        else:
            raise ListaVazia('apostas por data')

#acoes sorteio
    def add_sorteio(self, sorteio: Sorteio):
        if isinstance(sorteio, Sorteio) and sorteio not in self.__sorteios:
            self.__sorteios.append(sorteio)
        else:
            raise JaExiste('sorteio')

    def del_sorteio(self, sorteio: Sorteio):
        if isinstance(sorteio, Sorteio) and sorteio in self.__sorteios:
            self.__sorteios.remove(sorteio)
        else:
            raise NaoExiste('sorteio')

    def sorteios(self):
        return sorted(self.__sorteios, key= lambda x : x.data)

    def apostas_ganhas(self): 
        apostas = []
        for aposta in self.apostas():
            cont = 0
            for sorteio in self.sorteios():
                if (aposta.jogo.nome == sorteio.jogo.nome) and (sorteio.data - timedelta(days=7)<aposta.data<= sorteio.data):
                    for numero in sorteio.numeros:
                        if numero in aposta.numeros:
                            cont += 1
                    if cont == len(sorteio.numeros):
                        apostas.append(aposta)
        if len(apostas)>=1:
            return apostas
        else:
            raise ListaVazia('ganhadores')

    def ganhadores_por_jogo(self, jogo: Jogo):
        apostas = []
        apostas_jogo = self.apostas_por_jogo(jogo)
        apostas_ganhas = self.apostas_ganhas()
        for ap_ganha in apostas_ganhas:
            for ap_jogo in apostas_jogo:
                if ap_ganha == ap_jogo:
                    apostas.append(ap_ganha)
        if len(apostas) >= 1:
            return apostas
        else:
            raise ListaVazia('ganhadores por jogo')

    def ganhadores_por_data_jogo(self,  data_min: date, data_max: date, jogo = None):
        apostas_ganhas = self.apostas_ganhas()
        apostas = []
        apostas_data = self.apostas_por_data( data_min, data_max)
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
        if len(apostas) >= 1:
            return apostas
        else:
            raise ListaVazia('ganhadores')

    def ultimas_apostas_ganhas(self, qnt: int, jogo = None ):
        if len(self.apostas())>=1:
            if jogo is None:
                apostas = self.apostas_ganhas()[-qnt:]
            else:
                apostas = self.ganhadores_por_jogo(jogo)[-qnt:]
            return apostas
        else:
            raise ListaVazia('apostas ganhas')

    def sorteio_numeros_recorrentes(self, jogo: Jogo):
        # qnt de vezes q cada num foi apostado dentre as apostas ganhas
        apostas = self.ganhadores_por_jogo(jogo)
        if len(apostas) >= 1:
            numeros = {}
            for aposta in apostas:
                for numero in aposta.numeros:
                    if numero in numeros:
                        numeros[numero] = (numeros[numero] + 1)
                    else: 
                        numeros[numero] = 1

            return (sorted(numeros.items(), key= lambda x: x[1],reverse = True))
        else:
            raise ListaVazia('apostas ganhas do jogo')
