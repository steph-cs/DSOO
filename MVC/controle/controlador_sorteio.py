from entidade.sorteio import Sorteio
from limite.tela_sorteio import TelaSorteio

class ControladorSorteio():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_sorteio = TelaSorteio(self)
        self.__sorteios = []

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            1 : self.inclui_sorteio,
            2 : self.altera_sorteio,
            3 : self.exclui_sorteio,
            4 : self.lista_sorteio
        }
        op = True
        while op:
            opcao = self.__tela_sorteio.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def sorteios(self):
        return self.__sorteios

    def encontra_sorteio(self):
        #encontra o sorteio 
        info = self.__tela_sorteio.define_sorteio()
        existe = False 
        sorteio = None
        i = 0
        while existe is False and i< len(self.__sorteios):
            if (self.__sorteios[i].dia == info['dia']) and (self.__sorteios[i].mes == info['mes']) and (self.__sorteios[i].ano == info['ano']) and (self.__sorteios[i].jogo.nome == info['jogo']):
                sorteio = self.__sorteios[i]
                existe = True
                print("---Sorteio encontrado!---")
            else:
                i+=1
        if existe is False:
            print("Sorteio não encontrado!")
        return sorteio

    def inclui_sorteio(self):
        #inclui jogo
        info = self.__tela_sorteio.inclui_sorteio()
        sorteio = Sorteio(info['dia'],info['mes'],info['ano'],info['jogo'],info['numeros'])
        if sorteio not in self.__sorteios:
            self.__sorteios.append(sorteio)
            print("---Sorteio adicionado!---")
        else: 
            print("Sorteio já xiste!")

    def exclui_sorteio(self):
        #exclui sorteio
        sorteio = self.encontra_sorteio()
        if sorteio is not None:
            self.__sorteios.remove(sorteio)
            print("---Sorteio deletado!---")

    def lista_sorteio(self):
        # lista os sorteios
        if len(self.__sorteios) >= 1:
            print("-----Sorteios-----")
            for i in self.__sorteios:
                self.__tela_sorteio.lista_sorteio(i.dia, i.mes, i.ano, i.jogo, i.numeros)
        else:
            print("Não ha sorteios cadastrados!")

    def altera_sorteio(self):
        #opcoes de alteracao do sorteiodor
        switcher = {
            0 : False ,
            1 : self.altera_dia,
            2 : self.altera_mes,
            3 : self.altera_ano,
            4 : self.altera_jogo,
            5 : self.altera_numeros
        }
        op = True
        while op:
            opcao = self.__tela_sorteio.opcoes_alterar()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida()

    def altera_dia(self):
        #altera dia da sorteio
        sorteio = self.encontra_sorteio()
        if sorteio is not None:
            dia = self.__tela_sorteio.altera_dia()
            sorteio.dia = dia
            print("Dia alterado!")

    def altera_mes(self):
        #altera mes da sorteio
        sorteio = self.encontra_sorteio()
        if sorteio is not None:
            mes = self.__tela_sorteio.altera_mes()
            sorteio.mes = mes
            print("Mes alterado!")
    
    def altera_ano(self):
        #altera ano da sorteio
        sorteio = self.encontra_sorteio()
        if sorteio is not None:
            ano = self.__tela_sorteio.altera_ano()
            sorteio.ano = ano
            print("Ano alterado!")

    def altera_jogo(self):
        #altera jogo da sorteio
        sorteio = self.encontra_sorteio()
        if sorteio is not None:
            jogo = self.__tela_sorteio.altera_jogo()
            sorteio.jogo = jogo
            print("jogo alterado!")

    def altera_numeros(self):
        #altera numeros da sorteio
        sorteio = self.encontra_sorteio()
        if sorteio is not None:
            numeros = self.__tela_sorteio.altera_numeros()
            sorteio.numeros = numeros
            print("Numeros alterado!")

    