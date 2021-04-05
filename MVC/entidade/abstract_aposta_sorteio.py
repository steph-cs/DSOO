from datetime import date
from entidade.jogo import Jogo
from abc import ABC, abstractmethod
from entidade.exception import QuantidadeNumerosIncorreta, NumerosIncorretos


class Abstract_aposta_sorteio(ABC):
    @abstractmethod
    def __init__(self, data: date, jogo: Jogo):
        self.__data = data
        self.__jogo = jogo

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = data

    @property
    def jogo(self):
        return self.__jogo

    @jogo.setter
    def jogo(self, jogo: Jogo):
        if jogo.min_numeros <= len(self.numeros) <= jogo.max_numeros:
            self.__jogo = jogo
        else:
            raise QuantidadeNumerosIncorreta()
    
    @property
    @abstractmethod
    def numeros(self):
        pass
    
    @numeros.setter
    @abstractmethod
    def numeros(self):
        pass

    def num_rep(self, numeros: list):
        rep = False
        cont = 0
        while rep is False and cont< len(numeros):
            if (numeros.count(numeros[cont]) > 1) or numeros[cont] <= 0 or numeros[cont]>15:
                rep = True
            else:
                cont += 1
        return rep

