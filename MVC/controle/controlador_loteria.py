from limite.tela_loteria import TelaLoteria
from entidade.loteria import Loteria

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
            3 : self.consulta_apostas,
            4 : self.inclui_sorteio,
            5 : self.exclui_sorteio,
            6 : self.consulta_sorteios
        }
        op = True
        while op:
            opcao = self.__tela_loteria.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def inclui_aposta(self):
        aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta()
        if aposta is not None:
            if aposta not in self.__loteria.apostas():
                self.__loteria.add_aposta(aposta)
            else:
                print("Aposta ja existe!")

    def exclui_aposta(self):
        aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta()
        if aposta is not None:
            if aposta in self.__loteria.apostas():
                self.__loteria.del_aposta(aposta)
            else:
                print("Loteria nao contem aposta!")



    def consulta_apostas(self):
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
        if len(self.__loteria.apostas())>=1:
            for i in self.__loteria.apostas():
                self.__tela_loteria.lista_apostas(i.dia,i.mes,i.ano,i.jogo.nome,i.numeros)
        else:
            print("Nao ha apostas!")        

    def apostas_por_jogo(self):
        if len(self.__loteria.apostas())>=1:
            jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo()
            if jogo is not None:
                apostas = self.__loteria.apostas_por_jogo(jogo)
                for i in apostas:
                    self.__tela_loteria.lista_apostas(i.dia,i.mes,i.ano,i.jogo.nome,i.numeros)
        else:
            print("Nao ha apostas!")

    def apostas_por_data(self):
        if len(self.__loteria.apostas())>=1:
            data = self.__tela_loteria.pega_data()
            apostas = self.__loteria.apostas_por_data(data['dia'], data['mes'],data['ano'])
            for i in apostas:
                self.__tela_loteria.lista_apostas(i.dia,i.mes,i.ano,i.jogo.nome,i.numeros)    
        else:
            print("Nao ha apostas!")

    def apostas_por_jogo_data(self):
        if len(self.__loteria.apostas())>=1:
            jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo()
            data = self.__tela_loteria.pega_data()
            apostas = self.__loteria.apostas_por_jogo_data(jogo, data['dia'], data['mes'],data['ano'])
            for i in apostas:
                self.__tela_loteria.lista_apostas(i.dia,i.mes,i.ano,i.jogo.nome,i.numeros)
        else:
            print("Nao ha apostas!")



    def inclui_sorteio(self):
        sorteio = self.__controlador_sistema.controlador_sorteio().encontra_sorteio()
        if sorteio is not None:
            self.__loteria.add_sorteio(sorteio)
            print("Sorteio adicionado!")

    def exclui_sorteio(self):
        sorteio = self.__controlador_sistema.controlador_sorteio().encontra_sorteio()
        if sorteio is not None:
            self.__loteria.del_sorteio(sorteio)
            print("Sorteio deletado!")


    def consulta_sorteios(self):
        #opcoes consulta sorteios
        switcher = {
            0 : False ,
            1 : self.lista_sorteios,
            2 : self.apostas_ganhas,
            3 : self.ganhadores_por_jogo,
            4 : self.ganhadores_por_data,
            5 : self.ultimas_apostas_ganhas,
            6 : self.numeros_recorrentes
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
        if len(self.__loteria.sorteios())>=1:
            for i in self.__loteria.sorteios():
                self.__tela_loteria.lista_sorteios(i.dia,i.mes,i.ano,i.jogo.nome,i.numeros)
        else:
            print("Nao ha sorteios!")   

    def apostas_ganhas(self):
        if len(self.__loteria.apostas())>=1:
            apostas= self.__loteria.apostas_ganhas()
            for i in apostas:
                self.__tela_loteria.lista_apostas(i.dia,i.mes,i.ano,i.jogo.nome,i.numeros)
        else:
            print("Nao ha apostas!") 

    def ganhadores_por_jogo(self):
        #verifica se ha apostas na loteria; implementar abstrata
        if len(self.__loteria.apostas())>=1:
            # input define jogo e verifica a existencia
            jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo()
            if  jogo is not None:
                # pega apostas ganhas de acordo com o jogo
                apostas= self.__loteria.ganhadores_por_jogo(jogo)
                #titulo implementar classe abstrata
                print("-----{}------".format(jogo))
                for aposta in apostas:
                    # ve cada apostdor dentro das apostas ganhas
                    print("{}".format(aposta.numeros()))
                    for apostador in aposta.apostadores():
                        #aposta - [apostadores]
                        # imprime relatorio com 
                        self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf, aposta.dia, aposta.mes, aposta.ano)
        else:
            print("Nao ha apostas!") 

    def ganhadores_por_data(self):
        if len(self.__loteria.apostas())>=1:
            data = self.__tela_loteria.pega_data()
            apostas = self.__loteria.ganhadores_por_data_jogo(data['dia'],data['mes'],data['ano'])
            print("-----{}/{}/{}------".format(data['dia'],data['mes'],data['ano']))
            for aposta in apostas:
                # ve cada apostdor dentro das apostas ganhas
                print("{}".format(aposta.numeros()))
                for apostador in aposta.apostadores():
                    #aposta - [apostadores]
                    # imprime relatorio com 
                    self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf, aposta.dia, aposta.mes, aposta.ano)    
        else:
            print("Nao ha apostas!") 

    def ganhadores_por_jogo_data(self):
        if len(self.__loteria.apostas())>=1:
            jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo()
            data = self.__tela_loteria.pega_data()
            apostas = self.__loteria.ganhadores_por_data_jogo(data['dia'],data['mes'],data['ano'],jogo)
            print("-----{}------".format(jogo))
            for aposta in apostas:
                # ve cada apostdor dentro das apostas ganhas
                print("{}".format(aposta.numeros()))
                for apostador in aposta.apostadores():
                    #aposta - [apostadores]
                    # imprime relatorio com 
                    self.__tela_loteria.lista_ganhadores(apostador.nome,apostador.cpf,aposta.dia, aposta.mes, aposta.ano)


        else:
            print("Nao ha apostas!") 

    def ultimas_apostas_ganhas(self):
        pass

    def numeros_recorrentes(self):
        pass