from entidade.jogo import Jogo

from datetime import date, timedelta
from entidade.abstract_aposta_sorteio import Abstract_aposta_sorteio
from entidade.exception import QuantidadeNumerosIncorreta


class Sorteio(Abstract_aposta_sorteio):
    def __init__(self, data: date, jogo: Jogo, numeros: list):
        super().__init__(data, jogo)
        if len(numeros) == self.jogo.min_numeros and self.num_rep(numeros) is False:
            self.__numeros = numeros
        else:
            raise QuantidadeNumerosIncorreta()

    @property
    def numeros(self):
        return self.__numeros

    @numeros.setter
    def numeros(self, numeros: list):
        if len(self.__numeros) == self.jogo.min_numeros and self.num_rep(numeros) is False:
            self.__numeros = numeros
        else:
            raise QuantidadeNumerosIncorreta()
