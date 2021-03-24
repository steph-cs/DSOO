from entidade.jogo import Jogo
from datetime import date

class Aposta():
    def __init__(self, codigo, dia: int, mes: int, ano: int, jogo: Jogo, numeros: list):
        self.__codigo = codigo
        self.__dia = dia
        self.__mes = mes
        self.__ano = ano
        self.__data = date(ano,mes,dia)
        self.__jogo = jogo
        if self.__jogo.min_numeros <=len(numeros)<= self.__jogo.max_numeros:
            self.__numeros = numeros
        else:
            self.__numeros = None
        self.__apostadores = []

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

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
    def data(self):
        return self.__data

    @property
    def jogo(self):
        return self.__jogo

    @jogo.setter
    def jogo(self, jogo):
        self.__jogo = jogo

    @property
    def numeros(self):
        return self.__numeros

    @numeros.setter
    def numeros(self, numeros: list):
        if self.__jogo.min_numeros <=len(self.__numeros)<= self.__jogo.max_numeros:
            self.__numeros = numeros

    def num_rep(self):
        rep = False
        cont = 0
        while rep is False and cont< len(self.__numeros):
            if self.__numeros.count(self.__numeros[cont]) > 1:
                rep = True
            else:
                cont += 1
        return rep

    def add_apostador(self, apostador):
        from apostador import Apostador

        if isinstance(apostador, Apostador) and apostador not in self.__apostadores:
            if self.num_rep() is False:
                self.__apostadores.append(apostador)
                if self not in apostador.apostas():
                    apostador.add_aposta(self)
            else:
                print('Aposta com números repetidos')


    def del__apostador(self, apostador):
        from apostador import Apostador
        if isinstance(apostador, Apostador) and apostador in self.__apostadores:
            self.__apostadores.remove(apostador)
            if self in apostador.apostas():
                apostador.del_aposta(self)

    def apostadores(self):
        return self.__apostadores

