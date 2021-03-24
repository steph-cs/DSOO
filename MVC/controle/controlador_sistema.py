from limite.tela_sistema import TelaSistema

from controle.controlador_loteria import ControladorLoteria
from controle.controlador_apostador import ControladorApostador
from controle.controlador_aposta import ControladorAposta
from controle.controlador_jogo import ControladorJogo


class ControladorSistema:
    def __init__(self):
        self.__tela_sistema = TelaSistema(self)
        self.__controlador_loteria = ControladorLoteria(self)
        self.__controlador_apostador = ControladorApostador(self)
        self.__controlador_aposta = ControladorAposta(self)
        self.__controlador_jogo = ControladorJogo(self)

    def inicia(self):
        self.abre_tela_inicial()

    def controlador_apostador(self):
        return self.__controlador_apostador

    def controlador_aposta(self):
        return self.__controlador_aposta

    def controlador_jogo(self):
        return self.__controlador_jogo

    def controlador_loteria(self):
        return self.__controlador_loteria


    def abre_tela_inicial(self):
        switcher = {
            0 : False,
            1 : self.controlador_loteria(),
            2 : self.controlador_jogo(),
            3 : self.controlador_apostador(),
            4 : self.controlador_aposta()
        }
        op = True
        while op:
            opcao = self.__tela_sistema.mostra_tela_opcoes()
            funcao_escolhida = switcher[opcao]
            if funcao_escolhida is False:
                op = False
            else:
                funcao_escolhida.inicia()