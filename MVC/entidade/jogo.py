from entidade.exception import QuantidadeNumerosIncorreta

class Jogo():
    def __init__(self, nome: str, max_numeros: int, min_numeros: int, premio: float):
        self.__nome = nome
        if 0 < min_numeros <= max_numeros <= 15 :
            self.__max_numeros = max_numeros
            self.__min_numeros = min_numeros
        else:
            raise QuantidadeNumerosIncorreta()
        self.__premio = premio

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def max_numeros(self):
        return self.__max_numeros

    @max_numeros.setter
    def max_numeros(self, max_numeros: int):
        if self.__min_numeros <= max_numeros <= 15:
            self.__max_numeros = max_numeros
        else:
            raise QuantidadeNumerosIncorreta()

    @property
    def min_numeros(self):
        return self.__min_numeros

    @min_numeros.setter
    def min_numeros(self, min_numeros: int):
        if 0 < min_numeros <= self.__max_numeros:
            self.__min_numeros = min_numeros
        else:
            raise QuantidadeNumerosIncorreta()

    @property
    def premio(self):
        return self.__premio

    @premio.setter
    def premio(self, premio: float):
        self.__premio = premio
