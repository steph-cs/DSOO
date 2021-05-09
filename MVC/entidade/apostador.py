from entidade.pessoa import Pessoa
from entidade.endereco import Endereco

from entidade.exception import IdadeInvalida, JaExiste, ListaVazia, NaoExiste
class Apostador(Pessoa):
    def __init__(self, nome, cpf, ano_nascimento, estado, cidade):
        super().__init__(nome, cpf, ano_nascimento)
        self.__apostas = []
        self.__endereco = Endereco(estado, cidade)

    def add_aposta(self, aposta):
        from entidade.aposta import Aposta
        #se a aposta recebida é do tipo Aposta..
        if isinstance(aposta, Aposta):
            #se apostador nao possui a aposta..
            if aposta not in self.__apostas:
                #se o apostador tem +18
                if (self.idade >= 18):
                    #adiciona a aposta
                    self.__apostas.append(aposta)
                    #se a aposta nao possui o apostador..
                    if self not in aposta.apostadores():
                        #adiciona o apostador
                        aposta.add_apostador(self)
                else:
                    #se -18
                    raise IdadeInvalida()
            else:
                #se ja possuir a aposta
                raise JaExiste('Aposta')

    def del_aposta(self, aposta):
        from entidade.aposta import Aposta
        #se a aposta recebida é do tipo Aposta..
        if isinstance(aposta, Aposta):
            #se o apostador possui a aposta..
            if aposta in self.__apostas:
                #remove a aposta
                self.__apostas.remove(aposta)
                #se a aposta possui o apostador..
                if self in aposta.apostadores():
                    #remove o apostador
                    aposta.del_apostador(self)
            else:
                raise NaoExiste('aposta')
        
    def endereco(self):
        return self.__endereco

    def apostas(self):
        #retorna a lista de apostas que o apostador possui
        return self.__apostas
