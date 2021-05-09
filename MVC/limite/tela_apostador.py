import PySimpleGUI as sg
from limite.tela_abstrata import TelaAbstrata
from datetime import date, timedelta
from entidade.exception import CampoVazio
from entidade.exception import AnoInvalido

class TelaApostador(TelaAbstrata):
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__window = None

        self.__listagem = []
        self.__apostadores = []

        self.__apostas = []

        self.__idades = [i for i in range(1919,2021)]

    def listagem(self):
        return self.__listagem

    def init_components(self):
        #opcoes tela inicial
        
        botoes = [
            [sg.Button("EXCLUIR", key="excluir")],
            [sg.Button("ADD APOSTA", key="add-aposta")],
            [sg.Button("DEL APOSTA", key="del-aposta")]
        ]
        layout = [
            [sg.Text('Nome:'), sg.InputText(key="nome", size=(20, 1)),
            sg.Text('Cpf:'), sg.InputText(key="cpf", size=(20, 1)), 
            sg.Text('Ano nasc.:'), sg.InputCombo(self.__idades,size=(10, 1), key='nasc')],
            [sg.Text('Estado:'), sg.InputText(key="estado", size=(10, 1)),
            sg.Text('Cidade:'), sg.InputText(key="cidade", size=(20, 1))
            ,sg.Button("INCLUIR", key="incluir")],
            [sg.InputCombo(self.__apostadores, size=(20, 1), key='apostador-alterar'), 
            sg.Button("ALTERAR", key="alterar"),sg.Button("APOSTAS", key="apostas")],
            [sg.Listbox(values=(self.__listagem), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50,4), key='apostadores'),sg.Column(botoes)],
            [sg.Listbox(values=(self.__apostas), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50,4), key='apostas-geral')]
        ]
        self.__window = sg.Window('APOSTADOR').Layout(layout)
    
    def mostra_tela_opcoes(self):
        self.init_components()
        button, value = self.__window.Read()
        switcher = {
            'incluir' : self.inclui,
            'alterar' : self.altera,
            'excluir' : self.exclui,
            'apostas' : self.apostas,
            'add-aposta' : self.add_aposta,
            'del-aposta' : self.del_aposta
        }
        if button is None:
            return 0, None
        else:
            funcao_escolhida = switcher[button]
            info = funcao_escolhida(value)
            return button, info

    def apostas_geral(self, apostas):
        self.__apostas = apostas

    #opcoes
    def apostas(self, value):
        try:
            if value['apostador-alterar'] == '':
                raise CampoVazio()
            else:
                info = {}
                info['apostador'] = value['apostador-alterar']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def inclui(self, value):

        try:
            info = {}
            for i in ['nome','cpf','nasc','estado', 'cidade']:
                if value[i] == '':
                    raise CampoVazio()
                else:
                    info[i] = value[i]
            
            for i in ['nome','estado', 'cidade']:
                info[i] = (info[i]).capitalize()
            
            int(info['cpf'])

            if value['nasc'] in self.__idades:
                info['nasc'] = value['nasc']
            else:
                raise AnoInvalido()
    
            return info
        except CampoVazio as vazio:
            self.erro(vazio)
        except AnoInvalido as ano:
            self.erro(ano)
        except ValueError:
            self.erro('Cpf invalido')

    def altera(self, value):
        try:
            if value['apostador-alterar'] == '':
                raise CampoVazio()
            else:
                info = {}
                info['apostador'] = value['apostador-alterar']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def exclui(self, value):
        try:
            if len(value['apostadores']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['apostadores'] = value['apostadores']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def add_aposta(self, value):
        try:
            if len(value['apostadores']) == 0 or len(value['apostas-geral']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['apostadores'] = value['apostadores']
                info['apostas'] = value['apostas-geral']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def del_aposta(self, value):
        try:
            if len(value['apostadores']) == 0 or len(value['apostas-geral']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['apostadores'] = value['apostadores']
                info['apostas'] = value['apostas-geral']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    #listagem apostadores
    def listagem_apostador(self, nome, cpf, idade, estado, cidade):
        self.__apostadores.append(cpf)
        self.__listagem.append("{}   {}  {} anos  {} - {} ".format(cpf , nome, idade, estado, cidade))

    #listagem apostas
    def listagem_aposta(self, cod, jogo, data, num):
        self.__listagem.append("{} ->  {}  {}  {}".format(cod , jogo, data.strftime("%d/%m/%Y"), num))

    def tela_apostas(self):
        layout = [
            [sg.Listbox(values=(self.__listagem), size=(50,4), key='apostas')]
        ]
        self.__window = sg.Window('APOSTAS').Layout(layout)

    def mostra_tela_apostas(self):
        self.tela_apostas()
        button, value = self.__window.Read()
        self.close()

    #tela alteracao
    def tela_altera(self, nome, cpf, nasc, estado, cidade):
        
        layout = [
            [sg.Text('Nome:'), sg.InputText(nome ,key="nome", size=(20, 1)),
            sg.Text('Cpf:'), sg.InputText(cpf ,key="cpf", size=(20, 1)), 
            sg.Text('Ano nasc.:'), sg.InputCombo(self.__idades, nasc, size=(10, 1), key='nasc')],
            [sg.Text('Estado:'), sg.InputText(estado ,key="estado", size=(10, 1)),
            sg.Text('Cidade:'), sg.InputText(cidade ,key="cidade", size=(20, 1)),
            sg.Button("ALTERAR", key="alterar")]
        ]
        self.__window = sg.Window('APOSTADOR').Layout(layout)

    def mostra_tela_alterar(self, nome, cpf, nasc, estado, cidade):
        self.tela_altera(nome, cpf, nasc, estado, cidade)
        button, value = self.__window.Read()
        self.close()
        if button is None:
            return None
        else:
            infos = self.inclui(value) #valores escritos
            
            if infos is not None:
                apostador = [nome, cpf, nasc, estado, cidade]
                cont = 0
                infos_novas = {}
                for k,v in infos.items():
                    if v != apostador[cont]:
                        infos_novas[k] = infos[k]
                    cont +=1
                return infos_novas

    ###
    def limpar_listagem(self):
        self.__apostadores = []
        self.__listagem = []

    def close(self):
        self.__window.Close()