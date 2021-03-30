from limite.tela_aposta import TelaAposta
from entidade.aposta import Aposta
from controle.controlador_abstrato import ControladorAbstrato
from entidade.exception import JaExiste, NaoExiste, QuantidadeNumerosIncorreta, ListaVazia, IdadeInvalida


class ControladorAposta(ControladorAbstrato):
    def __init__(self,controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_aposta = TelaAposta(self)
        self.__apostas = []

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_aposta,
            2 : self.abre_tela_altera_aposta,
            3 : self.exclui_aposta,
            4 : self.lista_aposta,
            5 : self.lista_apostadores,
            6 : self.inclui_apostador,
            7 : self.exclui_apostador
        }
        op = True
        while op:
            opcao = self.__tela_aposta.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def encontra_aposta(self, msg: str):
        #encontra aposta pelo codigo
        codigo = self.__tela_aposta.pega_dado_int(msg)
        existe = False
        aposta = None
        i = 0
        while existe is False and i< len(self.__apostas):
            if self.__apostas[i].codigo == codigo:
                #se encontrado uma aposta com mesmo codigo...
                aposta = self.__apostas[i]
                existe = True
            else:
                i+=1
        return {'aposta': aposta, 'codigo': codigo}

    def encontra_aposta_existente(self, msg: str):
        #usada qnd é preciso que a aposta exista p realizar uma acao
        try:
            #pega e verifica a existencia da aposta
            aposta = self.encontra_aposta(msg)['aposta']
            if aposta is None:
                raise NaoExiste('Aposta')
            return aposta
        except NaoExiste as nao_existe:
            self.__tela_aposta.msg(nao_existe)

    def encontra_aposta_nao_existente(self, msg: str):
        #usada qnd é preciso que a aposta nao exista p realizar uma acao
        try:
            #pega e verifica a nao existencia da aposta
            aposta = self.encontra_aposta(msg)
            if aposta['aposta'] is not None:
                raise JaExiste('Aposta')
            return aposta['codigo']
        except JaExiste as ja_existe:
            self.__tela_aposta.msg(ja_existe)

    # acoes aposta
    def inclui_aposta(self):
        #inclui aposta
        #define se o jogo existe ou nao
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        #define se a aposta existe ou nao
        if jogo is not None:
            codigo = self.encontra_aposta_nao_existente('Codigo: ')
            if codigo is not None:
                #define a data
                data = self.__tela_aposta.pega_data()
                lido = True
                while lido:
                    try:
                        #define a lista de numeros 
                        numeros = self.__tela_aposta.leiaints()
                        #define o codigo
                        aposta = Aposta(codigo, data, jogo, numeros)
                        self.__apostas.append(aposta)
                        self.__tela_aposta.msg('Aposta Adicionada')
                        lido = False
                    except QuantidadeNumerosIncorreta as qnt_incorreta:
                        self.__tela_aposta.msg(qnt_incorreta)

    def exclui_aposta(self):
        #exclui aposta
        #pega o codigo e verifca a existencia da aposta..
        aposta = self.encontra_aposta_existente('Codigo da aposta para excluir: ')
        if aposta is not None:
            try:
                self.__apostas.remove(aposta)
                self.__tela_aposta.msg('Aposta Excluida')
            except NaoExiste as n_existe:
                self.__tela_aposta.msg(n_existe)

    def lista_aposta(self):
        # lista os apostas
        try:
            #se ha apostas para listar
            if len(self.__apostas) >= 1:
                self.__tela_aposta.msg('Apostas')
                for i in self.__apostas:
                    self.__tela_aposta.lista_apostas(i.codigo ,i.data, i.jogo.nome, i.numeros)
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_aposta.msg(vazia)

    # acoes altera aposta

    def abre_tela_altera_aposta(self):
        #opcoes de alteracao do apostador
        switcher = {
            0 : False ,
            1 : self.altera_codigo,
            2 : self.altera_data,
            3 : self.altera_jogo,
            4 : self.altera_numeros
        }
        op = True
        while op:
            opcao = self.__tela_aposta.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()
    
    def altera_codigo(self):
        #altera codigo da aposta
        #pede o codigo da aposta para alterar..
        aposta = self.encontra_aposta_existente('Codigo da aposta para alterar: ')
        if aposta is not None:
            #pede o novo codigo
            codigo = self.encontra_aposta_nao_existente('Novo codigo da aposta: ')
            if codigo is not None:
                #realiza a alteracao
                aposta.codigo = codigo
                self.__tela_aposta.msg('Codigo alterado')
           
    def altera_data(self):
        #altera data da aposta
        #pede o codigo da aposta para alterar..
        aposta = self.encontra_aposta_existente('Codigo da aposta para alterar: ')
        if aposta is not None:
            #pede a nova data
            self.__tela_aposta.msg('Nova data')
            data = self.__tela_aposta.pega_data()
            #realiza a alteracao
            aposta.data = data
            self.__tela_aposta.msg('Data alterada')

    def altera_jogo(self):
        #pede o codigo da aposta para alterar..
        aposta = self.encontra_aposta_existente('Codigo da aposta para alterar: ')
        if aposta is not None:
            jogo = self.__controlador_sistema.controlador_jogo().encontra_aposta_existente('Novo jogo: ')
            if jogo is not None:
                #realiza a alteracao
                try:
                    aposta.jogo = jogo
                    self.__tela_aposta.msg('Jogo alterado')
                except QuantidadeNumerosIncorreta as qnt_incorreta:
                    self.__tela_aposta.msg(qnt_incorreta)

    def altera_numeros(self):
        #pede o codigo da aposta para alterar..
        aposta = self.encontra_aposta_existente('Codigo da aposta para alterar: ')
        if aposta is not None:
            try:
                numeros = self.__tela_aposta.leiaints()
                aposta.numeros = numeros
                self.__tela_aposta.msg('Numeros alterados')
            except QuantidadeNumerosIncorreta as qnt_incorreta:
                self.__tela_aposta.msg(qnt_incorreta)

    #acoes apostador
    def inclui_apostador(self):
        #inclui apostador
        aposta = self.encontra_aposta_existente('Codigo da aposta: ')
        if aposta is not None:
            apostador = self.__controlador_sistema.controlador_apostador().encontra_apostador_existente('Cpf do apostador: ')
            if apostador is not None:
                try:
                    if apostador not in aposta.apostadores():
                        #realiza a inclusao
                        aposta.add_apostador(apostador)
                        self.__tela_aposta.msg('Apostador Adicionado')
                    else:
                        raise JaExiste('apostador')
                except JaExiste as ja_existe:
                    self.__tela_aposta.msg(ja_existe)
                except IdadeInvalida as idade:
                     self.__tela_aposta.msg(idade)

    def exclui_apostador(self):
        #exclui apostador
        aposta = self.encontra_aposta_existente('Codigo da aposta: ')
        if aposta is not None:
            apostador = self.__controlador_sistema.controlador_apostador().encontra_apostador_existente('Cpf do apostador: ')
            if apostador is not None:
                try:
                    if apostador in aposta.apostadores():
                        #realiza a exclusao
                        aposta.del_apostador(apostador)
                        self.__tela_aposta.msg('Apostador Excluido')
                    else:
                        raise NaoExiste('apostador')
                except NaoExiste as nao_existe:
                    self.__tela_aposta.msg(nao_existe)
    
    def lista_apostadores(self):
        aposta = self.encontra_aposta_existente('Codigo da aposta: ')
        if aposta is not None:
            try:
                if len(aposta.apostadores())>=1:
                    self.__tela_aposta.msg('Apostadores')
                    for i in aposta.apostadores():
                        self.__tela_aposta.lista_apostadores(i.nome, i.cpf, i.idade)
                else:
                    raise ListaVazia('apostadores')
            except ListaVazia as vazia:
                self.__tela_aposta.msg(vazia)

