from limite.tela_apostador import TelaApostador
from entidade.apostador import Apostador
from entidade.endereco import Endereco
from entidade.exception import JaExiste, NaoExiste, QuantidadeNumerosIncorreta, ListaVazia, IdadeInvalida
from persistencia.apostador_dao import ApostadorDAO

class ControladorApostador:
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_apostador = TelaApostador(self)
        self.__dao = ApostadorDAO()
    
    def __new__(cls, *args, **kwargs):
        if ControladorApostador.__instance is None:
            ControladorApostador.__instance = object.__new__(cls)
        return ControladorApostador.__instance

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            'incluir' : self.inclui_apostador,
            'alterar' : self.abre_tela_altera_apostador,
            'excluir' : self.exclui_apostador,
            'apostas' : self.lista_apostas,
            'add-aposta' : self.inclui_aposta,
            'del-aposta' : self.exclui_aposta
        }
        op = True
        while op:
            self.lista_apostador()
            self.__controlador_sistema.controlador_aposta().lista_aposta()
            apostas = (self.__controlador_sistema.controlador_aposta().listagem())
            self.__tela_apostador.apostas_geral(apostas)
            button, info = self.__tela_apostador.mostra_tela_opcoes()
            funcao_escolhida = switcher[button]
            if funcao_escolhida is False:
                op = False
            else:
                self.__tela_apostador.close()
                funcao_escolhida(info)

#listagens
    def listagem(self):
        return self.__tela_apostador.listagem()

    def apostadores(self):
        return {key: value for key, value in sorted(self.__dao.get_all().items(), key = lambda x: x[1].cpf)}

    def lista_apostador(self):
        self.__tela_apostador.limpar_listagem()
        if len(self.__dao.get_all()) >= 1:
            for i in self.apostadores().values():
                self.__tela_apostador.listagem_apostador(i.nome, i.cpf,i.idade, i.endereco().estado, i.endereco().cidade)

#inclusao/exclusao 
    def inclui_apostador(self, infos: dict):
        if infos is not None:
            cpf = infos['cpf']
            try:
                self.__dao.get_all()[cpf] 
            except KeyError:
                nome = infos['nome']
                ano_nasc = infos['nasc']
                estado = infos['estado']
                cidade = infos['cidade']
                #se nao existente pega o resto dos dados
                #cria e inclui o jogo
                apostador = Apostador(nome, cpf, ano_nasc, estado, cidade)
                self.__dao.add(cpf, apostador)
            else:
                self.__tela_apostador.erro('Apostador Ja Existe!')

    def exclui_apostador(self, infos: dict):
        #exclui apostador
        #pega o cpf e verifca a existencia do apostador..
        if infos is not None:
            try:
                for apostador in infos['apostadores']:
                    self.__dao.remove(apostador.split()[0])
            except KeyError:
                self.__tela_apostador.erro('Apostador Nao Existe!')
        
#alteracao
    def abre_tela_altera_apostador(self, info: dict):
        if info is not None:
            try:
                apostador = self.__dao.get(info['apostador'])
                cpf = apostador.cpf
                nome = apostador.nome
                ano_nasc = apostador.ano_nascimento
                estado = apostador.endereco().estado
                cidade = apostador.endereco().cidade
                infos = self.__tela_apostador.mostra_tela_alterar(nome, cpf, ano_nasc, estado, cidade)
                if infos is not None:
                    for i in ['nome', 'cpf', 'nasc','estado', 'cidade']:
                        if i in infos:
                            switcher = {
                            'nome' : self.altera_nome,
                            'cpf' : self.altera_cpf,
                            'nasc' : self.altera_ano_nascimento,
                            'estado' : self.altera_estado,
                            'cidade' : self.altera_cidade
                            }
                            switcher[i](apostador, infos[i])       
            except KeyError:
                self.__tela_apostador.erro('Apostador nao existe!')

    def altera_estado(self, apostador, estado):
        apostador.endereco().estado = estado
        self.__dao.add(apostador.cpf, apostador)

    def altera_cidade(self, apostador, cidade):
        apostador.endereco().cidade = cidade
        self.__dao.add(apostador.cpf, apostador)

    def altera_nome(self, apostador, nome):
        #altera nome do apostador
        apostador.nome = nome
        self.__dao.add(apostador.cpf, apostador)
    
    def altera_cpf(self, apostador, cpf):
        try:
            self.__dao.get(cpf)
            self.__tela_apostador.erro('Apostador ja existe!')
        except KeyError:
            self.__dao.remove(apostador.cpf)
            apostador.cpf = cpf
            self.__dao.add(cpf, apostador)

    def altera_ano_nascimento(self, apostador, ano_nasc):
        #altera ano de nascimento do apostador
        apostador.ano_nascimento = ano_nasc
        self.__dao.add(apostador.cpf, apostador)

#acoes aposta
    def inclui_aposta(self, infos: dict):
        if infos is not None:
            try:
                for apostador in infos['apostadores']:
                    apostador = self.__dao.get(apostador.split()[0])
                    for aposta in infos['apostas']:
                        aposta = self.__controlador_sistema.controlador_aposta().apostas()[aposta.split()[0]]
                        try:
                            apostador.add_aposta(aposta)
                        except JaExiste as ja_existe:
                            self.__tela_apostador.erro(ja_existe)
                        except IdadeInvalida as idade:
                            self.__tela_apostador.erro(idade)
            except KeyError:
                self.__tela_aposta.erro('Apostador Nao Existe!')

    def exclui_aposta(self, infos: dict):
        if infos is not None:
            try:
                for apostador in infos['apostadores']:
                    apostador = self.__dao.get(apostador.split()[0])
                    for aposta in infos['apostas']:
                        aposta = self.__controlador_sistema.controlador_aposta().apostas()[aposta.split()[0]]
                        #realiza a inclusao
                        try:
                            apostador.del_aposta(aposta)
                        except NaoExiste as n_existe:
                            self.__tela_apostador.erro(n_existe)
            except KeyError:
                self.__tela_aposta.erro('Aposta Nao Existe!')

    def lista_apostas(self, infos: dict):
        #pega o cpf e verifica sua existencia
        if infos is not None:
            try:
                apostador = self.__dao.get(infos['apostador'])
                self.__tela_apostador.limpar_listagem()
                #se o apostador existir..
                if len(apostador.apostas()) >= 1:
                    #se ha apostas para listar
                    for i in apostador.apostas():
                        self.__tela_apostador.listagem_aposta(i.codigo, i.jogo.nome, i.data, i.numeros)
                    self.__tela_apostador.mostra_tela_apostas()
                else:
                    raise ListaVazia('apostas')
            except ListaVazia as vazia:
                self.__tela_apostador.erro(vazia)

