from entidade.jogo import Jogo
from limite.tela_jogo import TelaJogo
from entidade.exception import JaExiste, NaoExiste, QuantidadeNumerosIncorreta, ListaVazia

class ControladorJogo():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_jogo = TelaJogo(self)
        self.__jogos = []

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_jogo,
            2 : self.abre_tela_altera_jogo,
            3 : self.exclui_jogo,
            4 : self.lista_jogo
        }
        op = True
        while op:
            opcao = self.__tela_jogo.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def jogos(self):
        return self.__jogos

    def encontra_jogo(self, msg: str):
        nome = self.__tela_jogo.pega_dado_str(msg)
        existe = False 
        jogo = None
        i = 0
        while existe is False and i< len(self.__jogos):
            if self.__jogos[i].nome == nome:
                #se encontrado um jogo com mesmo nome...
                jogo = self.__jogos[i]
                existe = True
            else:
                i+=1
        return {'jogo':jogo, 'nome': nome}

    def encontra_jogo_existente(self, msg: str):
        #usada qnd é preciso que o jogo exista p realizar uma acao
        try:
            #pega e verifica a existencia do jogo
            jogo = self.encontra_jogo(msg)['jogo']
            if jogo is None:
                raise NaoExiste('Jogo')
            return jogo
        except NaoExiste as nao_existe:
            self.__tela_jogo.msg(nao_existe)
        # retorna o jogo se encontrado ou None

    def encontra_jogo_nao_existente(self, msg: str):
        #usada qnd é preciso que o jogo nao exista p realizar uma acao
        try:
            #pega e verifica a existencia do jogo
            jogo = self.encontra_jogo(msg)
            if jogo['jogo'] is not None:
                raise JaExiste('Jogo')
            return jogo['nome']
        except JaExiste as ja_existe:
            self.__tela_jogo.msg(ja_existe)
        # retorna o nome do jogo se nenhum igual encontrado ou None

    def inclui_jogo(self):
        #pega e verifca a nao existencia do jogo..
        jogo = self.encontra_jogo_nao_existente('Nome do jogo: ')
        if jogo is not None:
            lido = True
            premio = self.__tela_jogo.pega_dado_int('Premio: ')
            while lido:
                try:        
                    #se nao existente pega o resto dos dados
                    max_num = self.__tela_jogo.pega_dado_int('Maximo de numeros: ')
                    min_num = self.__tela_jogo.pega_dado_int('Minimo de numeros: ')
                    #cria e inclui o jogo
                    jogo = Jogo(jogo, max_num, min_num, premio)
                    self.__jogos.append(jogo)
                    self.__tela_jogo.msg('Jogo Adicionado')
                    lido = False
                except QuantidadeNumerosIncorreta as qnt_incorreta:
                    self.__tela_jogo.msg(qnt_incorreta)

    def exclui_jogo(self):
        #exclui jogo
        #pede o nome do jogo para alterar..
        jogo = self.encontra_jogo_existente('Nome do jogo para excluir: ')
        if jogo is not None:
            self.__jogos.remove(jogo)
            self.__tela_jogo.msg('Jogo Excluido')

    def lista_jogo(self):
        # lista os jogos
        try:
            if len(self.__jogos) >= 1:
                self.__tela_jogo.msg('Jogos')
                for i in self.__jogos:
                    self.__tela_jogo.lista_jogo(i.nome, i.max_numeros, i.min_numeros, i.premio)
            else:
                raise ListaVazia('jogos')
        except ListaVazia as vazia:
            self.__tela_jogo.msg(vazia)

    def abre_tela_altera_jogo(self):
        #opcoes de alteracao do apostador
        switcher = {
            0 : False ,
            1 : self.altera_nome,
            2 : self.altera_max_numeros,
            3 : self.altera_min_numeros,
            4 : self.altera_premio
        }
        op = True
        while op:
            opcao = self.__tela_jogo.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def altera_nome(self):
        #altera nome do jogo
        #pede o nome do jogo para alterar..
        jogo = self.encontra_jogo_existente('Nome do jogo para alterar: ')
        if jogo is not None:
            #pede o novo nome..
            nome = self.encontra_jogo_nao_existente('Novo nome do jogo: ')
            #realiza a alteracao
            if nome is not None:
                jogo.nome = nome 
                self.__tela_jogo.msg('Nome alterado!')    

    def altera_max_numeros(self):
        #altera o max numeros
        #pede o nome do jogo para alterar..
        try:
            jogo = self.encontra_jogo_existente('Nome do jogo para alterar: ')
            if jogo is not None:
                #pede o novo max numeros..
                max_num = self.__tela_jogo.pega_dado_int('Novo maximo de numeros: ')
                #realiza a alteracao
                jogo.max_numeros = max_num
                self.__tela_jogo.msg('Maximo de numeros alterados')
        except QuantidadeNumerosIncorreta as qnt_incorreta:
            self.__tela_jogo.msg(qnt_incorreta)

    def altera_min_numeros(self):
        #altera o min numeros
        #pede o nome do jogo para alterar..
        try:
            jogo = self.encontra_jogo_existente('Nome do jogo para alterar: ')
            if jogo is not None:
                #pede o novo min numeros..
                min_numeros = self.__tela_jogo.pega_dado_int('Novo minimo de numeros: ')
                #realiza a alteracao
                jogo.min_numeros = min_numeros
        except QuantidadeNumerosIncorreta as qnt_incorreta:
            self.__tela_jogo.msg(qnt_incorreta)

    def altera_premio(self):
        #altera o premmio
        #pede o nome do jogo para alterar..
        jogo = self.encontra_jogo_existente('Nome do jogo para alterar: ')
        if jogo is not None:
            #pede o novo valor do premio..
            premio = self.__tela_jogo.pega_dado_int('Valor do premio: ')
            #realiza a alteracao
            jogo.premio = premio
