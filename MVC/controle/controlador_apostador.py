from limite.tela_apostador import TelaApostador
from entidade.apostador import Apostador

class ControladorApostador:
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_apostador = TelaApostador(self)
        self.__apostadores = []

    def apostadores(self):
        return self.__apostadores

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_apostador,
            2 : self.altera_apostador,
            3 : self.exclui_apostador,
            4 : self.lista_apostador,
            5 : self.lista_apostas,
            6 : self.inclui_aposta,
            7 : self.exclui_aposta
        }
        op = True
        while op:
            opcao = self.__tela_apostador.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def inclui_apostador(self):
        #inclui apostador
        info = self.__tela_apostador.inclui_apostador()
        apostador = Apostador(info['nome'],info['cpf'])
        if apostador not in self.__apostadores:
            self.__apostadores.append(apostador)
            print("---Apostador adicionado!---")
        else: 
            print("Apostador já xiste!")

    def exclui_apostador(self):
        #exclui apostador
        apostador = self.encontra_apostador()
        if apostador is not None:
            self.__apostadores.remove(apostador)
            print("---Apostador deletado!---")
       
    def encontra_apostador(self):
        #encontra o apostador pelo cpf
        cpf = self.__tela_apostador.define_apostador()
        existe = False
        apostador = None
        i = 0
        while existe is False and i< len(self.__apostadores):
            if self.__apostadores[i].cpf == cpf:
                apostador = self.__apostadores[i]
                existe = True
                print("---Apostador encontrado!---")
            else:
                i+=1
        if existe is False:
            print("Apostador não encontrado!")
        return apostador
        
    def altera_apostador(self):
        #opcoes de alteracao do apostador
        switcher = {
            0 : False ,
            1 : self.altera_nome,
            2 : self.altera_cpf
        }
        op = True
        while op:
            opcao = self.__tela_apostador.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def altera_nome(self):
        #altera nome do apostador
        apostador = self.encontra_apostador()
        if apostador is not None:
            nome = self.__tela_apostador.altera_nome()
            apostador.nome = nome
            print("Nome alterado!")

    def altera_cpf(self):
        #altera cpf do apostador
        apostador = self.encontra_apostador()
        if apostador is not None:
            cpf = self.__tela_apostador.altera_cpf()
            apostador.cpf = cpf
            print("Cpf alterado!")

    def lista_apostador(self):
        # lista os apostadores
        print("-----Apostadores-----")
        for i in self.__apostadores:
            self.__tela_apostador.lista_apostadores(i.nome, i.cpf)

    def lista_apostas(self):
        apostador = self.encontra_apostador()
        if apostador is not None:
            print("-------Apostas-------")
            for i in apostador.apostas():
                self.__tela_apostador.lista_apostas(i.dia, i.mes, i.ano, i.jogo.nome, i.numeros)

    def inclui_aposta(self):
        apostador = self.encontra_apostador()
        if apostador is not None:
            aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta()
            if aposta is not None and aposta:
                if aposta not in apostador.apostas:
                    apostador.add_aposta()
                    print("Aposta adicionada!")
                else:
                    print("Apostador já contem aposta!")

    def exclui_aposta(self):
        apostador = self.encontra_apostador()
        if apostador is not None:
            aposta = self.__controlador_sistema.controlador_aposta().encontra_aposta()
            if aposta is not None and aposta:
                if aposta in apostador.apostas:
                    apostador.add_aposta()
                    print("Aposta deletada!")
                else:
                    print("Apostador não contem aposta!")