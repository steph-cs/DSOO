from limite.tela_aposta import TelaAposta
from entidade.aposta import Aposta
from entidade.exception import JaExiste, NaoExiste, QuantidadeNumerosIncorreta, ListaVazia, IdadeInvalida, NumerosIncorretos
from persistencia.aposta_dao import ApostaDAO


class ControladorAposta:
    __instance = None

    def __init__(self,controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_aposta = TelaAposta(self)
        self.__dao = ApostaDAO()
    
    def __new__(cls, *args, **kwargs):
        if ControladorAposta.__instance is None:
            ControladorAposta.__instance = object.__new__(cls)
        return ControladorAposta.__instance

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            'incluir' : self.inclui_aposta,
            'alterar' : self.abre_tela_altera_aposta,
            'excluir' : self.exclui_aposta,
            'apostadores' : self.lista_apostadores,
            'add-apostador' : self.inclui_apostador,
            'del-apostador' : self.exclui_apostador
        }
        op = True
        while op:
            self.lista_aposta()

            self.listagem_jogos()

            self.listagem_geral_apostadores()
            button, info = self.__tela_aposta.mostra_tela_opcoes()
            funcao_escolhida = switcher[button]
            if funcao_escolhida is False:
                op = False
            else:
                self.__tela_aposta.close()
                funcao_escolhida(info)

    def listagem_jogos(self):
        control = self.__controlador_sistema.controlador_jogo()
        jogos = list((control.jogos().keys()))
        self.__tela_aposta.jogos(jogos)
    
    def listagem_geral_apostadores(self):
        self.__controlador_sistema.controlador_apostador().lista_apostador()
        apostadores = (self.__controlador_sistema.controlador_apostador().listagem())
        self.__tela_aposta.apostadores_geral(apostadores)

    def apostas(self):
        #retorna a lista de apostas ordenada por data
        return {key: value for key, value in sorted(self.__dao.get_all().items(), key = lambda x: x[1].data)}

# acoes aposta
    def inclui_aposta(self, infos: dict):
        if infos is not None:
            codigo = infos['cod']
            try:
                self.__dao.get_all()[codigo] 
            except KeyError:
                try:
                    jogo = self.__controlador_sistema.controlador_jogo().jogos()[infos['jogo']]
                    numeros = infos['num']
                    data = infos['data']
                    aposta = Aposta(codigo, data, jogo, numeros)
                    self.__dao.add(codigo, aposta)
                    self.__tela_aposta.erro('Aposta Adicionada!')
                except KeyError:
                    self.__tela_aposta.erro('Jogo nao existe!!')
                except QuantidadeNumerosIncorreta as qnt_incorreta:
                    #se qnt de num incorreta mostra o max e min permitido de acordo c o jogo escolhido
                    self.__tela_aposta.erro(
                    '''{}
                    Max: {}  Min: {}'''.format(qnt_incorreta, jogo.max_numeros, jogo.min_numeros))
                except NumerosIncorretos as num_incorretos:
                    self.__tela_aposta.erro(num_incorretos)    
            else:
                self.__tela_aposta.erro('Aposta Ja Existe!')

    def listagem(self):
        return self.__tela_aposta.listagem()

    def exclui_aposta(self, infos: dict):
        #exclui aposta
        if infos is not None:
            try:
                for aposta in infos['apostas']:
                    self.__dao.remove(aposta.split()[0])
            except KeyError:
                self.__tela_aposta.erro('Aposta Nao Existe!')

    def lista_aposta(self):
        # lista os aposta
        self.__tela_aposta.limpar_listagem()
        if len(self.__dao.get_all()) >= 1:
            for i in self.apostas().values():
                self.__tela_aposta.listagem_aposta(i.codigo, i.jogo.nome, i.data, i.numeros)

# acoes altera aposta

    def abre_tela_altera_aposta(self, info: dict):
        #opcoes de alteracao do apostador
        if info is not None:
            try:
                aposta = self.__dao.get(info['aposta'])
                cod = aposta.codigo
                jogo = aposta.jogo.nome
                data = aposta.data
                num = aposta.numeros
                
                infos = self.__tela_aposta.mostra_tela_alterar(cod, jogo, data, num)
            
                if infos is not None:
                    switcher = {
                        'cod' : self.altera_codigo,
                        'data' : self.altera_data,
                        'jogo' : self.altera_jogo,
                        'num' : self.altera_numeros
                    }
                    for i in ['cod', 'jogo', 'data', 'num']:
                        if i in infos:
                            switcher[i](aposta, infos[i])       
            except KeyError:
                self.__tela_aposta.erro('Aposta nao existe!')
            except QuantidadeNumerosIncorreta as qnt_incorreta:
                self.__tela_aposta.erro(qnt_incorreta)
            except NumerosIncorretos as num_incorretos:
                self.__tela_aposta.erro(num_incorretos)
    
    def altera_codigo(self, aposta, cod):
        try:
            self.__dao.get(cod)
            self.__tela_aposta.erro('Aposta ja existe!')
        except KeyError:
            self.__dao.remove(aposta.codigo)
            aposta.codigo = cod
            self.__dao.add(cod, aposta)
           
    def altera_data(self, aposta, data):
        #altera data da aposta
        self.__dao.remove(aposta.codigo)
        aposta.data = data
        self.__dao.add(aposta.codigo, aposta)
        
    def altera_jogo(self, aposta, jogo):
        try:
            jogo = self.__controlador_sistema.controlador_jogo().jogos()[jogo]
            self.__dao.remove(aposta.codigo)
            aposta.jogo = jogo
            self.__dao.add(aposta.codigo, aposta)
        except KeyError:
            self.__tela_aposta.erro('Jogo nao existe!!')

    def altera_numeros(self, aposta, numeros):
        #pede o codigo da aposta para alterar..
        self.__dao.remove(aposta.codigo)
        aposta.numeros = numeros
        self.__dao.add(aposta.codigo, aposta)

#acoes apostador
    def inclui_apostador(self, infos: dict):
        #inclui apostador
        if infos is not None:
            try:
                for aposta in infos['apostas']:
                    aposta = self.__dao.get(aposta.split()[0])
                    for apostador in infos['apostadores']:
                        apostador = self.__controlador_sistema.controlador_apostador().apostadores()[apostador.split()[0]]
                        #realiza a inclusao
                        try:
                            aposta.add_apostador(apostador)
                        except JaExiste as ja_existe:
                            self.__tela_aposta.erro(ja_existe)
                        except IdadeInvalida as idade:
                            self.__tela_aposta.erro(idade)
            except KeyError:
                self.__tela_aposta.erro('Aposta Nao Existe!')

    def exclui_apostador(self, infos: dict):
        if infos is not None:
            try:
                for aposta in infos['apostas']:
                    aposta = self.__dao.get(aposta.split()[0])
                    for apostador in infos['apostadores']:
                        apostador = self.__controlador_sistema.controlador_apostador().apostadores()[apostador.split()[0]]
                        try:
                            aposta.del_apostador(apostador)
                        except NaoExiste as n_existe:
                            self.__tela_aposta.erro(n_existe)
            except KeyError:
                self.__tela_aposta.erro('Aposta Nao Existe!')
    
    def lista_apostadores(self, infos: dict):
        if infos is not None:
            try:
                aposta = self.__dao.get(infos['aposta'])
                self.__tela_aposta.limpar_listagem()
                #se o apostador existir..
                if len(aposta.apostadores()) >= 1:
                    #se ha apostas para listar
                    for i in aposta.apostadores():
                        self.__tela_aposta.listagem_apostadores(i.nome, i.cpf, i.idade, i.endereco().estado, i.endereco().cidade)
                    self.__tela_aposta.mostra_tela_apostadores()
                else:
                    raise ListaVazia('apostadores')
            except ListaVazia as vazia:
                self.__tela_aposta.erro(vazia)

