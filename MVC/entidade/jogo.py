
class Jogo():
    def __init__(self, nome: str, max_numeros: int, min_numeros: int, premio: int):
        self.__nome = nome
        self.__max_numeros = max_numeros
        self.__min_numeros = min_numeros
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
        self.__max_numeros = max_numeros

    @property
    def min_numeros(self):
        return self.__min_numeros

    @min_numeros.setter
    def min_numeros(self, min_numeros: int):
        self.__min_numeros = min_numeros

    @property
    def premio(self):
        return self.__premio

    @premio.setter
    def premio(self, premio):
        self.__premio = premio
