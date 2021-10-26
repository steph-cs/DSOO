from limite.tela_loteria import TelaLoteria
from entidade.loteria import Loteria
from entidade.exception import QuantidadeNumerosIncorreta, NaoExiste, JaExiste, ListaVazia

class ControladorLoteria():
    __instance = None

    def __init__(self,controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_loteria = TelaLoteria(self)
        self.__loteria = Loteria()

    def __new__(cls, *args, **kwargs):
        if ControladorLoteria.__instance is None:
            ControladorLoteria.__instance = object.__new__(cls)
        return ControladorLoteria.__instance

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            'incluir' : self.inclui,
            'excluir' : self.exclui,
            'consulta-aposta' : self.abre_tela_consulta_apostas,
            'consulta-sorteio' : self.abre_tela_consulta_sorteios
        }
        op = True
        while op:
            self.__tela_loteria.limpar_listagem()

            self.listagem_apostas()
            self.listagem_sorteios()
            self.listagem_jogos()
            self.lista_apostas()
            self.lista_sorteios()

            button, info = self.__tela_loteria.mostra_tela_opcoes()
            funcao_escolhida = switcher[button]
            if funcao_escolhida is False:
                op = False
            else:
                self.__tela_loteria.close()
                funcao_escolhida(info)

#listagens
    def listagem_apostas(self):
        control = self.__controlador_sistema.controlador_aposta()
        control.lista_aposta()
        apostas = (control.listagem())
        self.__tela_loteria.apostas(apostas)

    def listagem_sorteios(self):
        control = self.__controlador_sistema.controlador_sorteio()
        control.lista_sorteio()
        sorteios = (control.listagem())
        self.__tela_loteria.sorteios(sorteios)

    def listagem_jogos(self):
        control = self.__controlador_sistema.controlador_jogo()
        jogos = list((control.jogos().keys()))
        self.__tela_loteria.jogos(jogos)
    
    def lista_apostas(self):
            if len(self.__loteria.apostas())>=1:
                for i in self.__loteria.apostas():
                    self.__tela_loteria.listagem_aposta_cad(i.codigo, i.jogo.nome, i.data, i.numeros)

    def lista_sorteios(self):
        if len(self.__loteria.sorteios())>=1:
            for i in self.__loteria.sorteios():
                self.__tela_loteria.listagem_sorteio_cad(i.codigo, i.data, i.jogo.nome, i.jogo.premio, i.numeros)

#inclusao/exclusao
    def inclui(self, infos: dict):
        if infos is not None:
            apostas = infos['apostas']
            if apostas is not None:
                for aposta in apostas:
                    try:
                        aposta = self.__controlador_sistema.controlador_aposta().apostas()[aposta.split()[0]]
                        self.inclui_aposta(aposta)
                    except NaoExiste as n_existe:
                        self.__tela_loteria.erro(n_existe)
            sorteios = infos['sorteios']
            if sorteios is not None:
                for sorteio in sorteios:
                    sorteio = self.__controlador_sistema.controlador_sorteio().sorteios()[sorteio.split()[0]]
                    self.inclui_sorteio(sorteio)
    
    def exclui(self, infos: dict):
        if infos is not None:
            apostas = infos['apostas-cad']
            if apostas is not None:
                for aposta in apostas:
                    try:
                        aposta = self.__controlador_sistema.controlador_aposta().apostas()[aposta.split()[0]]
                        self.exclui_aposta(aposta)
                    except NaoExiste as n_existe:
                        self.__tela_loteria.erro(n_existe)
            sorteios = infos['sorteios-cad']
            if sorteios is not None:
                for sorteio in sorteios:
                    sorteio = self.__controlador_sistema.controlador_sorteio().sorteios()[sorteio.split()[0]]
                    self.exclui_sorteio(sorteio)

#acoes aposta
    def inclui_aposta(self, aposta):
        try:
            self.__loteria.add_aposta(aposta)
        except JaExiste as existe:
            self.__tela_loteria.erro(existe)

    def exclui_aposta(self, aposta):
        try:
            self.__loteria.del_aposta(aposta)
        except NaoExiste as n_existe:
            self.__tela_loteria.erro(n_existe)


    def abre_tela_consulta_apostas(self, info: dict):
        if info is not None:
            try:
                opcao = info['opcao']
                switcher = {
                    'jogo' : self.apostas_por_jogo,
                    'data' : self.apostas_por_data,
                    'data-jogo' : self.apostas_por_jogo_data
                }
                op = {
                    'jogo': {'jogo': info['jogo']}, 
                    'data': {'min':info['min'],'max':info['max']},
                    'data-jogo':{'jogo': info['jogo'],'min':info['min'],'max':info['max']}
                    }
                for k,v in op.items():
                    if k == opcao:
                        switcher[opcao](v) 
            except KeyError:
                self.__tela_loteria.erro('Opcao invalida!')
            except ListaVazia as vazia:
                self.__tela_loteria.erro(vazia)

    def apostas_por_jogo(self, info: dict):
        if None not in info.values():
            try:
                if len(self.__loteria.apostas())>=1:
                    jogo = self.__controlador_sistema.controlador_jogo().jogos()[info['jogo']]
                    apostas = self.__loteria.apostas_por_jogo(jogo)
                    for i in apostas:
                        self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
                    self.__tela_loteria.mostra_tela_listagem()
                else:
                    raise ListaVazia('apostas')
            except KeyError:
                self.__tela_loteria.erro('Jogo nao existe')
        else:
            raise KeyError()

    def apostas_por_data(self, info: dict):
        if None not in info.values():
            if len(self.__loteria.apostas())>=1:
                apostas = self.__loteria.apostas_por_data(info['min'], info['max'])
                for i in apostas:
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
                self.__tela_loteria.mostra_tela_listagem()
            else:
                raise ListaVazia('apostas')
        else:
            raise KeyError()

    def apostas_por_jogo_data(self,info: dict):
        if None not in info.values():
            if len(self.__loteria.apostas())>=1:
                jogo = self.__controlador_sistema.controlador_jogo().jogos()[info['jogo']]
                apostas = self.__loteria.apostas_por_jogo_data(jogo, info['min'], info['max'])
                for i in apostas:
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
                self.__tela_loteria.mostra_tela_listagem()
            else:
                raise ListaVazia('apostas') 
        else:
            raise KeyError()

#acoes sorteio
    def inclui_sorteio(self, sorteio):
        try:
            self.__loteria.add_sorteio(sorteio)
        except JaExiste as existe:
            self.__tela_loteria.erro(existe)

    def exclui_sorteio(self, sorteio):
        try:
            self.__loteria.del_sorteio(sorteio)
        except NaoExiste as n_existe:
            self.__tela_loteria.erro(n_existe)

    def abre_tela_consulta_sorteios(self, info: dict):
        #opcoes consulta sorteios
        if info is not None:
            try:
                opcao = info['opcao']
                switcher = {
                    'apostas ganhas' : self.apostas_ganhas,
                    'ganhadores' : self.ganhadores,
                    'num recorrentes' : self.numeros_recorrentes
                }
                op = {
                    'apostas ganhas' : {'jogo': info['jogo'], 'qnt': info['qnt']},
                    'ganhadores': {'jogo': info['jogo'],'min':info['min'],'max':info['max']}, 
                    'num recorrentes':{'jogo': info['jogo']}
                }
                for k,v in op.items():
                    if k == opcao:
                        switcher[opcao](v) 
            except KeyError:
                self.__tela_loteria.erro('Opcao invalida!')
            except ListaVazia as vazia:
                self.__tela_loteria.erro(vazia)

    def apostas_ganhas(self, infos: dict):
        if infos['qnt'] is not None: 
            self.ultimas_apostas_ganhas(infos)
        else:
            try:
                if len(self.__loteria.apostas())>=1:
                    apostas= self.__loteria.apostas_ganhas()
                    self.__tela_loteria.info_listagem('{} apostas ganhas'.format(len(apostas)))
                    for i in apostas:
                        self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
                    self.__tela_loteria.mostra_tela_listagem()
                else:
                    raise ListaVazia('apostas ganhas')
            except ListaVazia as vazia:
                self.__tela_loteria.erro(vazia)

    def ultimas_apostas_ganhas(self, infos):
        if infos['qnt'] is not None or infos['jogo'] is not None:
            qnt = infos['qnt']
            try:
                if infos['jogo'] is not None:
                    jogo = self.__controlador_sistema.controlador_jogo().jogos()[infos['jogo']]
                    apostas = self.__loteria.ultimas_apostas_ganhas(qnt, jogo)   
                else:
                    apostas = self.__loteria.ultimas_apostas_ganhas(qnt)
                for i in apostas:    
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
                self.__tela_loteria.mostra_tela_listagem()
            except ListaVazia as vazia:
                self.__tela_loteria.erro(vazia)   
        else:
            raise KeyError()      

    def ganhadores(self, info: dict):
        #verifica se ha apostas na loteria; implementar abstrata
        if [i for i in info.values()].count(None) <=2:
            try:
                if len(self.__loteria.apostas())>=1:
                    try:
                        jogo = self.__controlador_sistema.controlador_jogo().jogos()[info['jogo']]
                        self.__tela_loteria.info_listagem('{}'.format(jogo.nome))
                        try:
                            if info['max'] != None and info['min'] != None:
                                apostas= self.__loteria.ganhadores_por_data_jogo(info['min'], info['max'], jogo)
                                self.__tela_loteria.info_listagem('Entre - {} - {}    {} apostas ganhas'.format(info['min'].strftime("%d/%m/%y"), info['max'].strftime("%d/%m/%y"), len(apostas)))
                            else:
                                raise KeyError()
                        except KeyError:
                            apostas= self.__loteria.ganhadores_por_jogo(jogo)
                            self.__tela_loteria.info_listagem('{} - {} apostas ganhas'.format(jogo.nome, len(apostas)))
                    except KeyError:
                        apostas= self.__loteria.ganhadores_por_data_jogo(info['min'], info['max'])
                        self.__tela_loteria.info_listagem('Entre - {} - {}    {} apostas ganhas'.format(info['min'].strftime("%d/%m/%y"), info['max'].strftime("%d/%m/%y"), len(apostas)))
                    
                    qnt_ganhadores = 0
                    for aposta in apostas:
                        qnt_ganhadores += len(aposta.apostadores())
                        for apostador in aposta.apostadores():
                            self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf, apostador.idade, aposta.data, aposta.jogo.premio, apostador.endereco().estado, apostador.endereco().cidade)
                        self.__tela_loteria.info_listagem('{} ganhadores'.format(qnt_ganhadores))
                    self.__tela_loteria.mostra_tela_listagem()
                else:
                    raise ListaVazia('apostas')
            except ListaVazia as vazia:
                self.__tela_loteria.erro(vazia)
        else:
            raise KeyError()

    def numeros_recorrentes(self, infos: dict):
        if infos['jogo'] is not None:
            jogo = self.__controlador_sistema.controlador_jogo().jogos()[infos['jogo']]
            numeros = self.__loteria.sorteio_numeros_recorrentes(jogo)
            for i in numeros:
                self.__tela_loteria.numeros_recorrentes(i[0], i[1])
            self.__tela_loteria.mostra_tela_listagem()
        else:
            raise KeyError()
        