from limite.tela_apostador import TelaApostador
from entidade.apostador import Apostador
from entidade.endereco import Endereco
from entidade.exception import JaExiste, NaoExiste, QuantidadeNumerosIncorreta, ListaVazia, IdadeInvalida

class ControladorApostador:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_apostador = TelaApostador(self)
        self.__apostadores = []

    def apostadores(self):
        return sorted(self.__apostadores, key= lambda x : x.idade)

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_apostador,
            2 : self.abre_tela_altera_apostador,
            3 : self.exclui_apostador,
            4 : self.lista_apostador,
            5 : self.lista_apostas,
            6 : self.inclui_aposta,
            7 : self.exclui_aposta,
            8 : self.altera_endereco
        }
        op = True
        while op:
            opcao = self.__tela_apostador.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def encontra_apostador(self, msg: str):
        #encontra o apostador pelo cpf
        cpf = self.__tela_apostador.pega_cpf(msg)
        existe = False
        apostador = None
        i = 0
        while existe is False and i< len(self.__apostadores):
            if self.__apostadores[i].cpf == cpf:
                #se encontrado um apostador com mesmo cpf...
                apostador = self.__apostadores[i]
                existe = True
            else:
                i+=1
        return {'apostador':apostador, 'cpf': cpf}

    def encontra_apostador_existente(self, msg: str):
        #usada qnd é preciso que o apostador exista p realizar uma acao
        try:
            #pega e verifica a existencia do apostador
            apostador = self.encontra_apostador(msg)['apostador']
            if apostador is None:
                raise NaoExiste('Apostador')
            return apostador
        except NaoExiste as nao_existe:
            self.__tela_apostador.msg(nao_existe)

    def encontra_apostador_nao_existente(self, msg: str):
        #usada qnd é preciso que o apostador nao exista p realizar uma acao
        try:
            #pega e verifica a nao existencia do apostador
            apostador = self.encontra_apostador(msg)
            if apostador['apostador'] is not None:
                raise JaExiste('Apostador')
            return apostador['cpf']
        except JaExiste as ja_existe:
            self.__tela_apostador.msg(ja_existe)
        
    #acoes apostador    
    def inclui_apostador(self):
        #inclui apostador
        #pega o cpf e verifca a nao existencia do apostador..
        cpf = self.encontra_apostador_nao_existente('Cpf: ')
        if cpf is not None:
            #se nao existente pega o resto dos dados
            #pega o nome..
            nome = self.__tela_apostador.pega_dado_str('Nome: ')
            estado = self.__tela_apostador.pega_dado_str('Estado: ')
            cidade = self.__tela_apostador.pega_dado_str('Cidade: ')
            lido = True
            while lido:
                try:
                    ano_nasc = self.__tela_apostador.pega_dado_int('Ano de nascimento: ')
                    #cria e inclui o apostador
                    apostador = Apostador(nome, cpf, ano_nasc, estado, cidade)
                    self.__apostadores.append(apostador)
                    self.__tela_apostador.msg('Apostador Adicionado')
                    lido = False
                except ValueError:
                    self.__tela_apostador.msg('Idade invalida!')

    def exclui_apostador(self):
        #exclui apostador
        #pega o cpf e verifca a existencia do apostador..
        apostador = self.encontra_apostador_existente('Cpf do apostador para excluir: ')
        if apostador is not None:
            self.__apostadores.remove(apostador)
            self.__tela_apostador.msg('Apostador Excluido')
        
    def lista_apostador(self):
        # lista os apostadores
        try:
            #se ha apostadores para listar
            if len(self.__apostadores)>=1:
                self.__tela_apostador.msg('Apostadores')
                for i in self.apostadores():
                    self.__tela_apostador.lista_apostadores(i.nome, i.cpf, i.idade, i.endereco().estado, i.endereco().cidade)
            else:
                raise ListaVazia('apostadores')
        except ListaVazia as vazia:
            self.__tela_apostador.msg(vazia)

    #alteracao
    def abre_tela_altera_apostador(self):
        #opcoes de alteracao do apostador
        switcher = {
            0 : False ,
            1 : self.altera_nome,
            2 : self.altera_cpf,
            3 : self.altera_ano_nascimento
        }
        op = True
        while op:
            opcao = self.__tela_apostador.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def altera_endereco(self):
        apostador = self.encontra_apostador_existente('Cpf do apostador: ')
        estado = self.__tela_apostador.pega_dado_str('Estado: ')
        cidade = self.__tela_apostador.pega_dado_str('Cidade: ')
        apostador.altera_endereco(estado, cidade)

    def altera_nome(self):
        #altera nome do apostador
        apostador = self.encontra_apostador_existente('Cpf do apostador para alterar: ')
        if apostador is not None:
            nome = self.__tela_apostador.pega_dado_str('Novo nome do apostador: ')
            apostador.nome = nome
            self.__tela_apostador.msg('Nome alterado')
    
    def altera_cpf(self):
        #altera cpf do apostador
        #pede o cpf do apostador para alterar..
        apostador = self.encontra_apostador_existente('Cpf do apostador para alterar: ')
        if apostador is not None:
            #pede o novo cpf..
            cpf = self.encontra_apostador_nao_existente('Novo cpf do apostador: ')
            if cpf is not None:
                #realiza a alteracao
                apostador.cpf = cpf
                self.__tela_apostador.msg('Cpf alterado')

    def altera_ano_nascimento(self):
        #altera ano de nascimento do apostador
        #pede o cpf do apostador para alterar..
        apostador = self.encontra_apostador_existente('Cpf do apostador para alterar: ')
        if apostador is not None:
            #pede o novo ano nascimento
            lido = True
            while lido:
                try:
                    ano_nasc = self.__tela_apostador.pega_dado_int('Novo ano de nascimento: ')
                    #realiza a alteracao
                    apostador.ano_nascimento = ano_nasc
                    self.__tela_apostador.msg('Ano de nascimento alterado')
                except ValueError:
                    self.__tela_apostador.msg('Ano invalido')

    #acoes aposta
    def inclui_aposta(self):
        #pega o cpf e verifica sua existencia
        apostador = self.encontra_apostador_existente('Cpf do apostador: ')
        #se o apostador existir..
        if apostador is not None:
            #pega a aposta..
            aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta_existente('Codigo da aposta: ')
            # se a aposta existir..
            if aposta is not None:
                try:
                    apostador.add_aposta(aposta)
                    self.__tela_apostador.msg('Aposta adicionada!')
                except JaExiste as ja_existe:
                    self.__tela_apostador.msg(ja_existe)
                except IdadeInvalida as idade:
                    self.__tela_apostador.msg(idade)

    def exclui_aposta(self):
        #pega o cpf e verifica sua existencia
        apostador = self.encontra_apostador_existente('Cpf do apostador: ')
        #se o apostador existir..
        if apostador is not None:
            #pega a aposta..
            aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta_existente('Codigo da aposta: ')
            # se a aposta existir..
            if aposta is not None:
                try:
                    apostador.del_aposta()
                except NaoExiste as nao_existe:
                    self.__tela_apostador.msg(nao_existe)

    def lista_apostas(self):
        #pega o cpf e verifica sua existencia
        apostador = self.encontra_apostador_existente('Cpf do apostador: ')
         #se o apostador existir..
        if apostador is not None:
            try:
                if len(apostador.apostas()) >= 1:
                    #se ha apostas para listar
                    self.__tela_apostador.msg('Apostas')
                    for i in apostador.apostas():
                        self.__tela_apostador.lista_apostas(i.codigo, i.data, i.jogo.nome, i.numeros)
                else:
                    raise ListaVazia('apostas')
            except ListaVazia as vazia:
                self.__tela_apostador.msg(vazia)

