from limite.tela_aposta import TelaAposta
from entidade.aposta import Aposta

class ControladorAposta():
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
            2 : self.altera_aposta,
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

    

    # acoes aposta
    def inclui_aposta(self):
        #inclui aposta
        jogo = self.__controlador_sistema.controlador_jogo().encontra_jogo()
        if jogo is not None:
            info = self.__tela_aposta.inclui_aposta()
            if jogo is not None:
                aposta = Aposta(info[0],info[1],info[2],info[3],jogo, info[4])
                if aposta.numeros is not None:
                    if aposta not in self.__apostas:
                        self.__apostas.append(aposta)
                        print("---Aposta adicionada!---")
                    else: 
                        print("Aposta já xiste!")
                else:
                    print("Numeros, invalidos")

    def exclui_aposta(self):
        aposta = self.encontra_aposta()
        if aposta is not None:
            self.__apostas.remove(aposta)
            print("Aposta deletada!")
       
    def encontra_aposta(self):
        #encontra aposta pelo codigo
        codigo = self.__tela_aposta.define_aposta()
        existe = False
        aposta = None
        i = 0
        while existe is False and i< len(self.__apostas):
            if self.__apostas[i].codigo == codigo:
                aposta = self.__apostas[i]
                existe = True
                print("---Aposta encontrada!---")
            else:
                i+=1
        if existe is False:
            print("Aposta não encontrada!")
        return aposta

    def lista_aposta(self):
        # lista os apostas
        print("-----Apostas-----")
        for i in self.__apostas:
            self.__tela_aposta.lista_apostas(i.dia, i.mes, i.ano, i.jogo.nome, i.numeros)

    # acoes altera aposta

    def altera_aposta(self):
        #opcoes de alteracao do apostador
        switcher = {
            0 : False ,
            1 : self.altera_codigo,
            2 : self.altera_dia,
            3 : self.altera_mes,
            4 : self.altera_ano,
            5 : self.altera_jogo,
            6 : self.altera_numeros
        }
        op = True
        while op:
            opcao = self.__tela_aposta.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida
    
    
    def altera_codigo(self):
        aposta = self.encontra_aposta()
        if aposta is not None:
            codigo = self.__tela_aposta.altera_codigo()
            aposta.codigo = codigo
            print("Codigo alterado!")

    def altera_dia(self):
        #altera dia da aposta
        aposta = self.encontra_aposta()
        if aposta is not None:
            dia = self.__tela_aposta.altera_dia()
            aposta.dia = dia
            print("Dia alterado!")

    def altera_mes(self):
        #altera mes da aposta
        aposta = self.encontra_aposta()
        if aposta is not None:
            mes = self.__tela_aposta.altera_mes()
            aposta.mes = mes
            print("Mes alterado!")
    
    def altera_ano(self):
        #altera ano da aposta
        aposta = self.encontra_aposta()
        if aposta is not None:
            ano = self.__tela_aposta.altera_ano()
            aposta.ano = ano
            print("Ano alterado!")

    def altera_jogo(self):
        aposta = self.encontra_aposta()
        if aposta is not None:
            jogo = self.__tela_aposta.altera_jogo()
            aposta.jogo = jogo
            print("Jogo alterado!")

    def altera_numeros(self):
        aposta = self.encontra_aposta()
        if aposta is not None:
            dia = self.__tela_aposta.altera_dia()
            aposta.dia = dia
            print("Dia alterado!")

    
    #acoes apostador
    def inclui_apostador(self):
        #inclui apostador
        aposta = self.encontra_aposta()
        if aposta is not None:
            apostador = self.__controlador_sistema.controlador_apostador().encontra_apostador()
            if apostador is not None:
                if apostador not in aposta.apostadores():
                    aposta.add_apostador(apostador)
                    print("---Apostador adicionado!---")
                else: 
                    print("Apostador já xiste!")

    def exclui_apostador(self):
        #exclui apostador
        aposta = self.encontra_aposta()
        if aposta is not None:
            apostador = self.__controlador_sistema.controlador_apostador().encontra_apostador()
            if apostador is not None:
                if apostador in aposta.apostadores():
                    aposta.del_apostador(apostador)
                    print("---Apostador deletado da aposta!---")
                else: 
                    print("Aposta nao contem apostador!")
    
    def lista_apostadores(self):
        aposta = self.encontra_aposta()
        if aposta is not None:
            print("-------Apostadores-------")
            for i in aposta.apostadores():
                self.__tela_aposta.lista_apostadores(i.nome, i.cpf)

