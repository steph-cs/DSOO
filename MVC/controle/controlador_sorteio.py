from entidade.sorteio import Sorteio
from limite.tela_sorteio import TelaSorteio
from entidade.exception import JaExiste, NaoExiste, ListaVazia, QuantidadeNumerosIncorreta

class ControladorSorteio():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_sorteio = TelaSorteio(self)
        self.__sorteios = []

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_sorteio,
            2 : self.abre_tela_altera_sorteio,
            3 : self.exclui_sorteio,
            4 : self.lista_sorteio
        }
        op = True
        while op:
            opcao = self.__tela_sorteio.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def sorteios(self):
        return self.__sorteios

    def encontra_sorteio(self, jogo, data):
        #encontra o sorteio 
        sorteio = None
        existe = False 
        i = 0
        while existe is False and i< len(self.__sorteios):
            if (self.__sorteios[i].data == data) and (self.__sorteios[i].jogo.nome == jogo):
                sorteio = self.__sorteios[i]
                existe = True
            else:
                i+=1
        return sorteio
    
    def encontra_sorteio_existente(self, msg_jogo: str, msg_data: str):
        #usada qnd é preciso que o sorteio exista p realizar uma acao
        try:
            #pega e verifica a existencia do sorteio
            sorteio = self.encontra_sorteio(msg_jogo , msg_data)
            if sorteio is None:
                raise NaoExiste('Sorteio')
            return sorteio
        except NaoExiste as nao_existe:
            self.__tela_sorteio.msg(nao_existe)
        # retorna o sorteio se encontrado ou None

    def encontra_sorteio_nao_existente(self, msg_jogo: str, msg_data: str):
        #usada qnd é preciso que o sorteio nao exista p realizar uma acao
        try:
            #pega e verifica a existencia do sorteio
            sorteio = self.encontra_sorteio(msg_jogo, msg_data)
            if sorteio['sorteio'] is not None:
                raise JaExiste('Sorteio')
            return sorteio
        except JaExiste as ja_existe:
            self.__tela_sorteio.msg(ja_existe)
        # retorna os dados do sorteio se nenhum igual encontrado ou None

    def inclui_sorteio(self):
        #inclui sorteio
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = self.__tela_sorteio.pega_data()
                #verifica(jogo,data) --> n deve exestir
                sorteio = self.encontra_sorteio(jogo, data)
                if sorteio is None:
                    numeros = self.__tela_sorteio.leiaints()
                    self.__sorteios.append(Sorteio(data, jogo, numeros))
                    self.__tela_sorteio.msg('Sorteio adicionado!')
                else:
                    raise JaExiste('sorteio')
            except JaExiste as ja_existe:
                self.__tela_sorteio.msg(ja_existe)        

    def exclui_sorteio(self):
        #exclui sorteio
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = self.__tela_sorteio.pega_data()
                #verifica(jogo,data) --> deve exestir
                sorteio = self.encontra_sorteio(jogo, data)
                if sorteio is not None:
                    self.__sorteios.remove(sorteio)
                    self.__tela_sorteio.msg('Sorteio deletado')
                else:
                    raise NaoExiste('sorteio')
            except NaoExiste as n_existe:
                self.__tela_sorteio.msg(n_existe)

    def lista_sorteio(self):
        # lista os sorteios
        try:
            if len(self.__sorteios) >= 1:
                self.__tela_sorteio.msg('Sorteios')
                for i in self.__sorteios:
                    self.__tela_sorteio.lista_sorteio(i.data, i.jogo.nome,i.jogo.premio, i.numeros)
            else:
                raise ListaVazia('sorteios')
        except ListaVazia as vazia:
            self.__tela_sorteio.msg(vazia)

    def abre_tela_altera_sorteio(self):
        #opcoes de alteracao do sorteiodor
        switcher = {
            0 : False ,
            1 : self.altera_data,
            2 : self.altera_jogo,
            3 : self.altera_numeros,
        }
        op = True
        while op:
            opcao = self.__tela_sorteio.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def altera_data(self):
        #altera data da sorteio
        #pega jogo, data verifica a existencia do sorteio
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = self.__tela_sorteio.pega_data()
                #verifica(jogo,data) --> deve exestir
                sorteio = self.encontra_sorteio(jogo, data)
                if sorteio is not None:
                    self.__tela_sorteio.msg('Nova data')
                    #nova data
                    nova_data = self.__tela_sorteio.pega_data()
                    #verifica(jogo, nova data) --> n deve existir
                    if self.encontra_sorteio(jogo, nova_data) is None:
                        sorteio.data = nova_data
                        self.__tela_sorteio.msg('Data alterada!')
                    else:
                        raise JaExiste('sorteio')
                else:
                    raise NaoExiste('sorteio')
            except NaoExiste as n_existe:
                self.__tela_sorteio.msg(n_existe)
            except JaExiste as existe:
                self.__tela_sorteio.msg(existe)

    def altera_jogo(self):
        #altera jogo da sorteio
        #pega jogo, data verifica a existencia do sorteio
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = self.__tela_sorteio.pega_data()
                #verifica(jogo,data) --> deve exestir
                sorteio = self.encontra_sorteio(jogo, data)
                if sorteio is not None:
                    #pega o novo jogo e verifica a nao existencia do sorteio 
                    novo_jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do novo jogo: ')
                    #verifica(novo jogo, data) --> n deve existir
                    if self.encontra_sorteio(novo_jogo, data) is None:
                        sorteio.jogo = novo_jogo
                        self.__tela_sorteio.msg('Jogo alterado!')
                    else:
                        raise JaExiste('sorteio')
                else:
                    raise NaoExiste('sorteio')
            except NaoExiste as n_existe:
                self.__tela_sorteio.msg(n_existe)
            except JaExiste as existe:
                self.__tela_sorteio.msg(existe)
            except QuantidadeNumerosIncorreta as qnt_incorreta:
                self.__tela_sorteio.msg(qnt_incorreta)

    def altera_numeros(self):
        #altera numeros da sorteio
        #pega jogo, data verifica a existencia do sorteio
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = self.__tela_sorteio.pega_data()
                #verifica(jogo,data) --> deve exestir
                sorteio = self.encontra_sorteio(jogo, data)
                if sorteio is not None:
                    numeros = self.__tela_sorteio.leiaints()
                    sorteio.numeros = numeros
                    self.__tela_sorteio.msg('Numeros alterados!')
                else:
                    raise NaoExiste('sorteio')
            except NaoExiste as n_existe:
                self.__tela_sorteio.msg(n_existe)
            except QuantidadeNumerosIncorreta as qnt_incorreta:
                self.__tela_sorteio.msg(qnt_incorreta)

    