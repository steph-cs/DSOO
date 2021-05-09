from entidade.jogo import Jogo
from datetime import date
from entidade.abstract_aposta_sorteio import Abstract_aposta_sorteio
from entidade.exception import QuantidadeNumerosIncorreta, IdadeInvalida, JaExiste, NaoExiste, ListaVazia, NumerosIncorretos

class Aposta(Abstract_aposta_sorteio):
    def __init__(self, codigo: int, data: date, jogo: Jogo, numeros: list):
        super().__init__(data, codigo)
        #e se a qnt de numeros esta dentro dos limites e nao ha rep..
        if jogo.min_numeros <=len(numeros)<= jogo.max_numeros:
            if self.num_rep(numeros) is False: 
                self.__numeros = numeros
                self.__jogo = jogo
            else:
                raise NumerosIncorretos()
        else:
            raise QuantidadeNumerosIncorreta()
    
        self.__apostadores = []

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
    def numeros(self):
        return self.__numeros

    @numeros.setter
    def numeros(self, numeros: list):
        num_rep = self.num_rep(numeros)
        limite = self.jogo.min_numeros <=len(numeros)<= self.jogo.max_numeros
        if limite:
            if (num_rep is False): 
                self.__numeros = numeros
            else:
                raise NumerosIncorretos()
        else:
            raise QuantidadeNumerosIncorreta()

    def add_apostador(self, apostador):
        from entidade.apostador import Apostador
        # se apostador do tipo Apostador
        if isinstance(apostador, Apostador):
            #se aposta nao possui apostador
            if (apostador not in self.__apostadores):
                #se apostado +18
                if (apostador.idade >= 18):
                    #adiciona o apostador
                    self.__apostadores.append(apostador)
                    #se o apostador nao possui a aposta
                    if self not in apostador.apostas():
                        #adiciona a aposta
                        apostador.add_aposta(self)
                else:
                    raise IdadeInvalida()
            else:
                raise JaExiste('apostador')

    def del_apostador(self, apostador):
        from entidade.apostador import Apostador
        # se apostador do tipo Apostador
        if isinstance(apostador, Apostador):
            #se a aposta possui o apostador
            if apostador in self.__apostadores:
                #remove o apostador
                self.__apostadores.remove(apostador)
                #se o apostador possui a aposta
                if self in apostador.apostas():
                    #remove a aposta
                    apostador.del_aposta(self)
            else:
                raise NaoExiste('apostador')

    def apostadores(self):
        return self.__apostadores
        