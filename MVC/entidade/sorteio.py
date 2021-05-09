from entidade.jogo import Jogo

from datetime import date, timedelta
from entidade.abstract_aposta_sorteio import Abstract_aposta_sorteio
from entidade.exception import QuantidadeNumerosIncorreta, NumerosIncorretos


class Sorteio(Abstract_aposta_sorteio):
    def __init__(self, codigo: str, data: date, jogo: Jogo, numeros: list):
        super().__init__(data, codigo)
        if jogo.min_numeros ==len(numeros):
            if self.num_rep(numeros) is False: 
                self.__jogo = jogo
                self.__numeros = numeros
            else:
                raise NumerosIncorretos()
        else:
            raise QuantidadeNumerosIncorreta()
  

    @property
    def jogo(self):
        return self.__jogo

    @jogo.setter
    def jogo(self, jogo: Jogo):
        if jogo.min_numeros == len(self.numeros) :
            self.__jogo = jogo
        else:
            raise QuantidadeNumerosIncorreta()

    @property
    def numeros(self):
        return self.__numeros

    @numeros.setter
    def numeros(self, numeros: list):
        num_rep = self.num_rep(numeros)
        limite = self.jogo.min_numeros == len(numeros)
        if limite:
            if (num_rep is False): 
                self.__numeros = numeros
            else:
                raise NumerosIncorretos()
        else:
            raise QuantidadeNumerosIncorreta()


