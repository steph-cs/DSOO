from entidade.jogo import Jogo

class Sorteio():
    def __init__(self, dia: int, mes: int,ano: int, jogo: Jogo, numeros: list):
        self.__dia = dia
        self.__mes = mes
        if isinstance(jogo, Jogo):
            self.__jogo = jogo
        self.__numeros = numeros
    
    @property
    def dia(self):
        return self.__dia

    @dia.setter
    def dia(self, dia):
        self.__dia = dia

    @property
    def mes(self):
        return self.__mes

    @mes.setter
    def mes(self, mes):
        self.__mes = mes

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, ano):
        self.__ano = ano

    @property
    def jogo(self):
        return self.__jogo

    @jogo.setter
    def jogo(self, jogo):
        if isinstance(jogo, Jogo):
            self.__jogo = jogo

    @property
    def numeros(self):
        return self.__numeros

    @numeros.setter
    def numeros(self, numeros: list):
        if len(self.__numeros) == self.__jogo.min_numeros and self.num_rep() is False:
            self.__numeros = numeros
        else:
            print('Verifique os numeros sorteados!')

    def num_rep(self):
        rep = False
        cont = 0
        while rep is False and cont< len(self.__numeros):
            if self.__numeros.count(self.__numeros[cont]) > 1:
                rep = True
            else:
                cont += 1
        return rep