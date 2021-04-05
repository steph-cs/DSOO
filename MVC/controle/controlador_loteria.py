from limite.tela_loteria import TelaLoteria
from entidade.loteria import Loteria
from entidade.exception import QuantidadeNumerosIncorreta, NaoExiste, JaExiste, ListaVazia

class ControladorLoteria():
    def __init__(self,controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_loteria = TelaLoteria(self)
        self.__loteria = Loteria()

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_aposta,
            2 : self.exclui_aposta,
            3 : self.abre_tela_consulta_apostas,
            4 : self.inclui_sorteio,
            5 : self.exclui_sorteio,
            6 : self.abre_tela_consulta_sorteios
        }
        op = True
        while op:
            opcao = self.__tela_loteria.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

#acoes aposta
    def inclui_aposta(self):
        aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta_existente('Codigo da aposta: ')
        try:
            if aposta is not None :
                self.__loteria.add_aposta(aposta)
                self.__tela_loteria.msg('Aposta Adicionada!')
        except NaoExiste as n_existe:
            self.__tela_loteria.msg(n_existe)
        except JaExiste as existe:
            self.__tela_loteria.msg(existe)

    def exclui_aposta(self):
        aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta_existente('Codigo da aposta: ')
        if aposta is not None and aposta:
            try:
                self.__loteria.del_aposta(aposta)
                self.__tela_loteria.msg('Aposta Deletada!')
            except NaoExiste as n_existe:
                self.__tela_loteria.msg(n_existe)

    def abre_tela_consulta_apostas(self):
        #opcoes consulta apostas
        switcher = {
            0 : False ,
            1 : self.lista_apostas,
            2 : self.apostas_por_jogo,
            3 : self.apostas_por_data,
            4 : self.apostas_por_jogo_data
        }
        op = True
        while op:
            opcao = self.__tela_loteria.opcoes_consulta_apostas()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()
    
    def lista_apostas(self):
        try:
            if len(self.__loteria.apostas())>=1:
                for i in self.__loteria.apostas():
                    self.__tela_loteria.lista_apostas(i.codigo ,i.data,i.jogo.nome,i.numeros)
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def apostas_por_jogo(self):
        try:
            if len(self.__loteria.apostas())>=1:
                jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
                if jogo is not None:
                    apostas = self.__loteria.apostas_por_jogo(jogo)
                    for i in apostas:
                        self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def apostas_por_data(self):
        try:
            if len(self.__loteria.apostas())>=1:
                datas = self.__tela_loteria.pega_datas()
                apostas = self.__loteria.apostas_por_data(datas['data_min'], datas['data_max'])
                for i in apostas:
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def apostas_por_jogo_data(self):
        try:
            if len(self.__loteria.apostas())>=1:
                jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
                datas = self.__tela_loteria.pega_datas()
                apostas = self.__loteria.apostas_por_jogo_data(jogo, datas['data_min'], datas['data_max'])
                for i in apostas:
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

#acoes sorteio
    def inclui_sorteio(self):
        controlador_sorteio = self.__controlador_sistema.controlador_sorteio()
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = controlador_sorteio.data_sorteio()
                sorteio = controlador_sorteio.encontra_sorteio(jogo, data)
                if sorteio is not None :
                    self.__loteria.add_sorteio(sorteio)
                    self.__tela_loteria.msg('Sorteio Adicionado!')
                else:
                    raise NaoExiste('sorteio')
            except NaoExiste as n_existe:
                self.__tela_loteria.msg(n_existe)
            except JaExiste as existe:
                self.__tela_loteria.msg(existe)

    def exclui_sorteio(self):
        controlador_sorteio = self.__controlador_sistema.controlador_sorteio()
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                data = controlador_sorteio.data_sorteio()
                sorteio =  controlador_sorteio.encontra_sorteio(jogo, data)
                if sorteio is not None:
                    self.__loteria.del_sorteio(sorteio)
                    self.__tela_loteria.msg('Sorteio Deletado!')
                else:
                    raise NaoExiste('sorteio')
            except NaoExiste as n_existe:
                self.__tela_loteria.msg(n_existe)

    def abre_tela_consulta_sorteios(self):
        #opcoes consulta sorteios
        switcher = {
            0 : False ,
            1 : self.lista_sorteios,
            2 : self.apostas_ganhas,
            3 : self.ganhadores_por_jogo,
            4 : self.ganhadores_por_data,
            5 : self.ganhadores_por_jogo_data,
            6 : self.ultimas_apostas_ganhas,
            7 : self.ultimas_apostas_ganhas_por_jogo,
            8 : self.numeros_recorrentes
        }
        op = True
        while op:
            opcao = self.__tela_loteria.opcoes_consulta_sorteios()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def lista_sorteios(self):
        try:
            if len(self.__loteria.sorteios())>=1:
                for i in self.__loteria.sorteios():
                    self.__tela_loteria.lista_sorteio(i.data, i.jogo.nome, i.jogo.premio, i.numeros)
            else:
                raise ListaVazia('sorteios')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def apostas_ganhas(self):
        try:
            if len(self.__loteria.apostas())>=1:
                apostas= self.__loteria.apostas_ganhas()
                self.__tela_loteria.msg('{} apostas ganhas'.format(len(apostas)))
                for i in apostas:
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
            else:
                raise ListaVazia('apostas ganhas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)    

    def ganhadores_por_jogo(self):
        #verifica se ha apostas na loteria; implementar abstrata
        try:
            if len(self.__loteria.apostas())>=1:
                # input define jogo e verifica a existencia
                jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
                if  jogo is not None:
                    # pega apostas ganhas de acordo com o jogo
                    apostas= self.__loteria.ganhadores_por_jogo(jogo)
                    if len(apostas)>=1:
                        self.__tela_loteria.msg('{} - {} apostas ganhas'.format(jogo.nome, len(apostas)))
                        qnt_ganhadores = 0
                        for aposta in apostas:
                            qnt_ganhadores += len(aposta.apostadores())
                            self.__tela_loteria.msg(aposta.numeros)
                            for apostador in aposta.apostadores():
                                self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf, apostador.idade, aposta.data, jogo.premio, apostador.endereco().estado, apostador.endereco().cidade)
                        self.__tela_loteria.msg('{} ganhadores'.format(qnt_ganhadores))
                    else:
                        raise ListaVazia('ganhadores por jogo')
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def ganhadores_por_data(self):
        try:
            if len(self.__loteria.apostas())>=1:
                datas = self.__tela_loteria.pega_datas()
                apostas = self.__loteria.ganhadores_por_data_jogo(datas['data_min'], datas['data_max'])
                if len(apostas)>=1:
                    self.__tela_loteria.msg('Entre - {} - {}    {} apostas ganhas'.format(datas['data_min'].strftime("%d/%m/%y"), datas['data_max'].strftime("%d/%m/%y"), len(apostas)))
                    qnt_ganhadores = 0
                    for aposta in apostas:
                        qnt_ganhadores += len(aposta.apostadores())
                        self.__tela_loteria.msg(aposta.numeros)
                        for apostador in aposta.apostadores():
                            self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf, apostador.idade, aposta.data, aposta.jogo.premio, apostador.endereco().estado, apostador.endereco().cidade)  
                    self.__tela_loteria.msg('{} ganhadores'.format(qnt_ganhadores))
                else:
                    raise ListaVazia('ganhadores por data')                              
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def ganhadores_por_jogo_data(self):
        try:
            if len(self.__loteria.apostas())>=1:
                jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
                datas = self.__tela_loteria.pega_datas()
                apostas = self.__loteria.ganhadores_por_data_jogo(datas['data_min'], datas['data_max'])
                if len(apostas)>=1:
                    self.__tela_loteria.msg('{} - {} apostas ganhas'.format(jogo.nome, len(apostas)))
                    qnt_ganhadores = 0
                    for aposta in apostas:
                        qnt_ganhadores += len(aposta.apostadores())
                        self.__tela_loteria.msg(aposta.numeros)
                        for apostador in aposta.apostadores():
                            self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf, apostador.idade, aposta.data, aposta.premio, apostador.endereco().estado, apostador.endereco().cidade) 
                    self.__tela_loteria.msg('{} ganhadores'.format(qnt_ganhadores))
                else:
                    raise ListaVazia('ganhadores por data')                              
            else:
                raise ListaVazia('apostas')
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def ultimas_apostas_ganhas(self):
        qnt = self.__tela_loteria.le_int('Quantidade de apostas: ')
        try:
            apostas = self.__loteria.ultimas_apostas_ganhas(qnt)
            for i in apostas:
                self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros)
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)

    def ultimas_apostas_ganhas_por_jogo(self):
        qnt = self.__tela_loteria.le_int('Quantidade de apostas: ')
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
        if jogo is not None:
            try:
                apostas = self.__loteria.ultimas_apostas_ganhas(qnt)
                for i in apostas:    
                    self.__tela_loteria.lista_apostas(i.codigo, i.data,i.jogo.nome,i.numeros) 
            except ListaVazia as vazia:
                self.__tela_loteria.msg(vazia)

    def numeros_recorrentes(self):
        try:
            jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo_existente('Nome do jogo: ')
            if jogo is not None:
                numeros = self.__loteria.sorteio_numeros_recorrentes(jogo)
                for i in numeros:
                    self.__tela_loteria.numeros_recorrentes(i[0], i[1])
        except ListaVazia as vazia:
            self.__tela_loteria.msg(vazia)
        