from entidade.pessoa import Pessoa

class Apostador(Pessoa):
    def __init__(self, nome, cpf):
        super().__init__(nome, cpf)
        self.__apostas = []

    def add_aposta(self, aposta):
        from entidade.aposta import Aposta
        
        if isinstance(aposta, Aposta) and aposta not in self.__apostas:
            if aposta.jogo.min_numeros <=len(aposta.numeros)<= aposta.jogo.max_numeros:
                if aposta.num_rep() is False:
                    self.__apostas.append(aposta)
                    if self not in aposta.apostadores():
                        aposta.add_apostador(self)
                else:
                    print('Aposta com números repetidos')
            else:
                print('Quantidade de numeros invalido')

    def del_aposta(self, aposta):
        from entidade.aposta import Aposta
        if isinstance(aposta, Aposta) and aposta in self.__apostas:
            self.__apostas.remove(aposta)
            if self in aposta.apostadores():
                aposta.del_apostador(self)

    def apostas(self):
        return self.__apostas