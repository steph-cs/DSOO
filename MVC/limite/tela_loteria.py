import PySimpleGUI as sg
from limite.tela_abstrata import TelaAbstrata
from entidade.exception import CampoVazio
from datetime import date

class TelaLoteria(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.__window = None
        
        self.__listagem = []
        
        self.__apostas_cadastradas = []
        self.__sorteios_cadastrados = []

        self.__apostas = []
        self.__sorteios = []
        self.__jogos = []

        self.__op_consulta_aposta = ['data','jogo','data-jogo']
        self.__op_consulta_sorteio = ['apostas ganhas','ganhadores','num recorrentes']

    def init_components(self):
        #opcoes tela inicial
        col_aposta = [
            [sg.Listbox(values=(self.__apostas), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(45,4), key='apostas',font=(8))]
        ]
        col_sorteio = [
            [sg.Listbox(values=(self.__sorteios), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(45,4), key='sorteios',font=(8))]
        ]

        col_aposta_cad = [
            [sg.Text('Opcao:',justification='center', size=(9,1)),
            sg.Text('Data min:',justification='center', size=(10,1)),
            sg.Text('Data max:',justification='center', size=(9,1)),
            sg.Text('Jogo:',justification='center', size=(7,1))],
            [sg.InputCombo(self.__op_consulta_aposta, size=(10, 1), key='op-consulta-aposta'),
            sg.InputText(size=(10, 1), key='data-min-aposta'),
            sg.InputText(size=(10, 1), key='data-max-aposta'),
            sg.InputCombo(self.__jogos,size=(7, 1), key='jogo-aposta'),
            sg.Button("->", key="consulta-aposta")],
            [sg.Listbox(values=(self.__apostas_cadastradas), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(45,4), key='apostas-cad',font=(8))]
        ]
        col_sorteio_cad = [
            [sg.Text('Opcao:',justification='center', size=(13,1)),
            sg.Text('Data min:',justification='center', size=(10,1)),
            sg.Text('Data max:',justification='center', size=(9,1)),
            sg.Text('Jogo:',justification='center', size=(7,1)),
            sg.Text('Qnt:',justification='center', size=(4,1))
            ],
            [sg.InputCombo(self.__op_consulta_sorteio, size=(15, 1), key='op-consulta-sorteio'),
            sg.InputText(size=(10, 1), key='data-min-sorteio'),
            sg.InputText(size=(10, 1), key='data-max-sorteio'),
            sg.InputCombo(self.__jogos,size=(7, 1), key='jogo-sorteio'),
            sg.InputText(size=(3, 1), key='qnt-sorteio'), 
            sg.Button("->", key="consulta-sorteio")],
            [sg.Listbox(values=(self.__sorteios_cadastrados), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(45,4), key='sorteios-cad',font=(8))]
        ]
        
        layout = [
            [sg.Text('APOSTAS/SORTEIOS', justification='center', size=(120,1))],
            [sg.Column(col_aposta),sg.Button("INCLUIR ", key="incluir"),sg.Column(col_sorteio)],
            [sg.Text('-'*240)],

            [sg.Text('APOSTAS/SORTEIOS CADASTRADOS', justification='center', size=(120,1))],
            [sg.Column(col_aposta_cad),sg.Button("EXCLUIR", key="excluir"),sg.Column(col_sorteio_cad)]          
        ]
        self.__window = sg.Window('APOSTA').Layout(layout)

    def mostra_tela_opcoes(self):
        self.init_components()
        button, value = self.__window.Read()
        switcher = {
            'incluir' : self.inclui,
            'excluir' : self.exclui,
            'consulta-aposta' : self.consulta_aposta,
            'consulta-sorteio' : self.consulta_sorteio
        }
        if button is None:
            return 0, None
        else:
            funcao_escolhida = switcher[button]
            info = funcao_escolhida(value)
            return button, info

    def listagem(self):
        return self.__listagem

    def apostas(self, apostas):
        self.__apostas = apostas
    
    def jogos(self, jogos):
        self.__jogos = jogos

    def sorteios(self, sorteios):
        self.__sorteios = sorteios

    #opcoes
    def inclui(self, value):
        try:
            info = {}
            if value['apostas'] == '' and value['sorteios'] == '':
                raise CampoVazio()

            for i in ['apostas','sorteios']:
                if value[i] != '':
                    info[i] = value[i]
                else:
                    info[i] = None
            
            return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def exclui(self, value):
        try:
            info = {}
            if value['apostas-cad'] == '' and value['sorteios-cad'] == '':
                raise CampoVazio()

            for i in ['apostas-cad','sorteios-cad']:
                if value[i] != '':
                    info[i] = value[i]
                else:
                    info[i] = None
            
            return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def consulta_aposta(self, value):
        try:
            info = {}

            #opcao
            if value['op-consulta-aposta'] == '' :
                raise CampoVazio()
            else:
                info['opcao'] = value['op-consulta-aposta']

            #dat minima e maxima
            datas = {'max': value['data-max-aposta'], 'min': value['data-min-aposta']}
            datas = self.verifica_data_max_min(datas)
            for k,v in datas.items():
                info[k] = v
            
            #jogo
            if  value['jogo-aposta'] != '':
                info['jogo'] = value['jogo-aposta']
            else:
                info['jogo'] = None
            
            if len(info)>=2:
                return info
            else:
                self.erro('Consulta Invalida!!')
        except CampoVazio as vazio:
            self.erro(vazio)

    def consulta_sorteio(self, value):
        try:
            info = {}
            if value['op-consulta-sorteio'] == '' :
                raise CampoVazio()
            else:
                info['opcao'] = value['op-consulta-sorteio']

            
            datas = {'max': value['data-max-sorteio'], 'min': value['data-min-sorteio']}
            datas = self.verifica_data_max_min(datas)
            for k,v in datas.items():
                info[k] = v

            if  value['jogo-sorteio'] != '':
                info['jogo'] = value['jogo-sorteio']
            else:
                info['jogo'] = None
                
            if value['qnt-sorteio'] != '':
                try:
                    info['qnt'] = int(value['qnt-sorteio'])
                except ValueError:
                    self.erro('Quantidade deve ser um numero inteiro!')
            else:
                info['qnt'] = None

            if info['opcao'] == 'apostas ganhas':
                return info
            elif [i for i in info.values()].count(None)<=3:
                return info
            else:
                self.erro('Consulta Invalida!!')
        except CampoVazio as vazio:
            self.erro(vazio)

#listagem
    def listagem_aposta_cad(self, cod, jogo, data, num):
        self.__apostas_cadastradas.append("{} ->  {}  {}  {}".format(cod , jogo, data.strftime("%d/%m/%Y"), num))

    def listagem_sorteio_cad(self, cod, data, jogo, premio, num):
        self.__sorteios_cadastrados.append("{} ->  {}  {}  R${:.2f}  {}".format(cod , data.strftime("%d/%m/%Y"),jogo, premio, num))

    def tela_listagem(self):
        layout = [
            [sg.Listbox(values=(self.__listagem), size=(80,10))]
        ]
        self.__window = sg.Window('LISTAGEM').Layout(layout)

    def mostra_tela_listagem(self):
        self.tela_listagem()
        button, value = self.__window.Read()

    def lista_apostas (self, cod, data, jogo, num):
        self.__listagem.append("{} ->  {}  {}  {}".format(cod , jogo, data.strftime("%d/%m/%Y"), num))

    
    def lista_ganhadores(self, nome: str, cpf: str, idade: int, data: date, premio: float, estado: str, cidade: str):
        self.__listagem.append(
        '''{} ->  {}  {} anos  {} - {}
        Data da aposta: {}    Premio: R${:.2f}
        '''.format(cpf,nome,  idade, estado, cidade, data.strftime("%d/%m/%y"), premio))

    def info_listagem(self, msg=''):
        self.__listagem.append(msg)
    
    def numeros_recorrentes(self, num: int, qnt_vezes: int):
        self.__listagem.append('Numero: {}    {} vezes'.format(num, qnt_vezes))
    

    def limpar_listagem(self):
        self.__apostas_cadastradas = []
        self.__sorteios_cadastrados = []
        self.__listagem = []
        
    def close(self):
        self.__window.Close()
    