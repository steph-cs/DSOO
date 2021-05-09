import PySimpleGUI as sg
from datetime import date, timedelta
from limite.tela_abstrata import TelaAbstrata
from entidade.exception import CampoVazio, CodigoInvalido

class TelaAposta(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.__window = None
        
        self.__listagem = []
        self.__apostas = []
        self.__jogos = []
        self.__apostadores = []

    def listagem(self):
        return self.__listagem

    def init_components(self):
        #opcoes tela inicial
        inclui = [
            [sg.Text('Codigo:'), sg.InputText(key="cod", size=(20, 1)),
            sg.Text('      Data:'), sg.InputText(key="data", size=(20, 1))],
            [sg.Text('Jogo:   '), sg.InputCombo(self.__jogos, key="jogo", size=(18, 1)),
            sg.Text('Numeros:'), sg.InputText(key="num", size=(20, 1))]
        ]
        botoes = [
            [sg.Button("EXCLUIR", key="excluir")],
            [sg.Button("ADD APOSTADOR", key="add-apostador")],
            [sg.Button("DEL APOSTADOR", key="del-apostador")]
        ]
        layout = [
            [sg.Column(inclui),
            sg.Button("INCLUIR", key="incluir")],
            [sg.InputCombo(self.__apostas, size=(20, 1), key='aposta-alterar'), 
            sg.Button("ALTERAR", key="alterar"),
            sg.Button("APOSTADORES", key="apostadores")],
            [sg.Listbox(values=(self.__listagem), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50,4), key='apostas'),sg.Column(botoes)],
            [sg.Listbox(values=(self.__apostadores), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50,4), key='apostadores-geral')]
        ]
        self.__window = sg.Window('APOSTA').Layout(layout)

    def apostadores_geral(self, apostadores):
        self.__apostadores = apostadores

    def jogos(self, jogos):
        self.__jogos = jogos

    def mostra_tela_opcoes(self):
        self.init_components()
        button, value = self.__window.Read()
        switcher = {
            'incluir' : self.inclui,
            'alterar' : self.altera,
            'excluir' : self.exclui,
            'apostadores' : self.apostadores,
            'add-apostador' : self.add_apostador,
            'del-apostador' : self.del_apostador
        }
        if button is None:
            return 0, None
        else:
            funcao_escolhida = switcher[button]
            info = funcao_escolhida(value)
            return button, info

    #opcoes
    def inclui(self, value):
        try:
            info = {}
            for i in ['cod', 'data', 'jogo','num']:
                if value[i] == '':
                    raise CampoVazio()
                else:
                    info[i] = value[i]

            try:
                for i in info['cod']:
                    int(i)
            except ValueError:
                raise CodigoInvalido()

            info['jogo'] = (value['jogo']).capitalize()

            #verificacao da data 00/00/0000
            info['data'] = self.verifica_data(value['data'])

            #verificacao da lista de numeros
            info['num'] = self.verifica_numeros(value['num'])

            if None not in info.values():
                return info
            
        except CodigoInvalido as cod:
            self.erro(cod)
        except CampoVazio as vazio:
            self.erro(vazio)
        except ValueError:
            self.erro('Codigo invalido')

    def altera(self, value):
        try:
            if value['aposta-alterar'] == '':
                raise CampoVazio()
            else:
                info = {}
                info['aposta'] = value['aposta-alterar']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def exclui(self, value):
        try:
            if len(value['apostas']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['apostas'] = value['apostas']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def add_apostador(self, value):
        try:
            if len(value['apostas']) == 0 or len(value['apostadores-geral']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['apostas'] = value['apostas']
                info['apostadores'] = value['apostadores-geral']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def del_apostador(self, value):
        try:
            if len(value['apostas']) == 0 or len(value['apostadores-geral']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['apostas'] = value['apostas']
                info['apostadores'] = value['apostadores-geral']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def apostadores(self, value):
        try:
            if value['aposta-alterar'] == '':
                raise CampoVazio()
            else:
                info = {}
                info['aposta'] = value['aposta-alterar']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)
    #listagem apostas
    def listagem_aposta(self, cod, jogo, data, num):
        self.__apostas.append(cod)
        self.__listagem.append("{} ->  {}  {}  {}".format(cod , jogo, data.strftime("%d/%m/%Y"), num))

    #listagem apostadores
    def listagem_apostadores(self, nome, cpf, idade, estado, cidade):
        #i.nome, i.cpf, i.idade, i.endereco().estado, i.endereco().cidade
        self.__listagem.append("{}   {}  {} anos  {} - {} ".format(cpf , nome, idade, estado, cidade))

    def tela_apostadores(self):
        layout = [
            [sg.Listbox(values=(self.__listagem), size=(50,10), key='apostadores')]
        ]
        self.__window = sg.Window('APOSTADORES').Layout(layout)

    def mostra_tela_apostadores(self):
        self.tela_apostadores()
        button, value = self.__window.Read()

    #tela alteracao
    def tela_altera(self, cod, jogo, data, num):
        layout = [
            [[[sg.Text('Codigo:'), sg.InputText(cod,key="cod", size=(20, 1)),
            sg.Text('Data:'), sg.InputText(data.strftime("%d/%m/%Y"),key="data", size=(20, 1))],
            [sg.Text('Jogo:'), sg.InputCombo(self.__jogos, jogo,key="jogo", size=(18, 1)),
            sg.Text('Numeros:'), sg.InputText(num,key="num", size=(20, 1))]],
            sg.Button("ALTERAR", key="alterar")]
        ]
        self.__window = sg.Window('APOSTA').Layout(layout)

    def mostra_tela_alterar(self, cod, jogo, data, num):
        self.tela_altera(cod, jogo, data, num)
        button, value = self.__window.Read()
        self.close()
        if button is None:
            return None
        else:
            value['num']= (str(value['num']).replace('(','').replace(')',''))
            infos = self.inclui(value) #valores escritos
            
            if infos is not None:
                aposta = [cod, data, jogo, num]
                cont = 0
                infos_novas = {}
                for k,v in infos.items():
                    if v != aposta[cont] and v is not None:
                        infos_novas[k] = infos[k]
                    cont +=1
                return infos_novas
    ####
    def limpar_listagem(self):
        self.__apostas = []
        self.__listagem = []

    def close(self):
        self.__window.Close()