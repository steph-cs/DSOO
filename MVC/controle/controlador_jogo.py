from entidade.jogo import Jogo
from limite.tela_jogo import TelaJogo

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
            2 : self.altera_jogo,
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

    def encontra_jogo(self):
        #encontra o jogo pelo nome
        nome = self.__tela_jogo.define_jogo()
        existe = False 
        jogo = None
        i = 0
        while existe is False and i< len(self.__jogos):
            if self.__jogos[i].nome == nome:
                jogo = self.__jogos[i]
                existe = True
                print("---Jogo encontrado!---")
            else:
                i+=1
        if existe is False:
            print("Jogo não encontrado!")
        return jogo

    def inclui_jogo(self):
        #inclui jogo
        info = self.__tela_jogo.inclui_jogo()
        jogo = Jogo(info[0],info[1],info[2],info[3])
        if jogo not in self.__jogos:
            self.__jogos.append(jogo)
            print("---Jogo adicionado!---")
        else: 
            print("Jogo já xiste!")

    def exclui_jogo(self):
        #exclui jogo
        jogo = self.encontra_jogo()
        if jogo is not None:
            self.__jogos.remove(jogo)
            print("---Jogo deletado!---")

    def lista_jogo(self):
        # lista os jogos
        if len(self.__jogos) >= 1:
            print("-----Jogos-----")
            for i in self.__jogos:
                self.__tela_jogo.lista_jogo(i.nome, i.max_numeros, i.min_numeros, i.premio)
        else:
            print("Não ha jogos cadastrados!")

    def altera_jogo(self):
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
        jogo = self.encontra_jogo()
        if jogo is not None:
            nome = self.__tela_jogo.altera_nome()
            jogo.nome = nome
            print("Nome alterado!")

    def altera_max_numeros(self):
        jogo = self.encontra_jogo()
        if jogo is not None:
            max_numeros = self.__tela_jogo.altera_max_numeros()
            jogo.max_numeros = max_numeros
            print("Maximo de numeros alterado!")

    def altera_min_numeros(self):
        jogo = self.encontra_jogo()
        if jogo is not None:
            min_numeros = self.__tela_jogo.altera_min_numeros()
            jogo.min_numeros = min_numeros
            print("Minimno de numeros alterado!")

    def altera_premio(self):
        jogo = self.encontra_jogo()
        if jogo is not None:
            premio = self.__tela_jogo.altera_premio()
            jogo.premio = premio
            print("Premio alterado!")