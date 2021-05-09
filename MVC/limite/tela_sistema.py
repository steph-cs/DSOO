from limite.tela_abstrata import TelaAbstrata
import PySimpleGUI as sg

class TelaSistema(TelaAbstrata):
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text('Opcoes:', justification='center', size=(22, 1), font=(15))],
            [sg.Button("Loteria", key='1', size=(25,2))],
            [sg.Button("Jogo", key='2', size=(25,2))],
            [sg.Button("Apostador", key='3', size=(25,2))],
            [sg.Button("Aposta", key='4', size=(25,2))],
            [sg.Button("Sorteio", key='5', size=(25,2))],
            [sg.Button("Sair", key='0', size=(25,2))]
        ]
        self.__window = sg.Window('Sistema').Layout(layout)   

    def mostra_tela_opcoes(self):
        self.init_components()
        button, value = self.__window.Read()
        if button is None:
            button = 0
        self.close()
        return int(button)

    def close(self):
        self.__window.Close()