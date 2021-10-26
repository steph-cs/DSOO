from limite.tela_abstrata import TelaAbstrata
import PySimpleGUI as sg
from entidade.exception import CampoVazio, CodigoInvalido


class TelaSorteio(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
    
        self.__window = None
        self.__listagem = []
        self.__sorteios = []
        self.__jogos = []

    def jogos(self, jogos):
        self.__jogos = jogos

    def listagem(self):
        return self.__listagem

    def init_components(self):
        #opcoes tela inicial
    
        inclusao = [
            [sg.Text('Cod:   '), sg.InputText(key="cod", size=(20, 1)),
            sg.Text('Data:   '), sg.InputText(key="data", size=(20, 1))],
            [sg.Text('Jogo:'), sg.InputCombo(self.__jogos,key="jogo", size=(20, 1)),
            sg.Text('Numeros:'), sg.InputText(key="num", size=(20, 1))
            ]
        ]
        layout = [
            [sg.Column(inclusao),sg.Button("INCLUIR", key="incluir")],
            [sg.InputCombo(self.__sorteios, size=(20, 1), key='sorteio-alterar'), 
            sg.Button("ALTERAR", key="alterar")],
            [sg.Listbox(values=(self.__listagem), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50,4), key='sorteios-excluir'),sg.Button("EXCLUIR", key="excluir")]
        ]
        self.__window = sg.Window('SORTEIOS').Layout(layout)

    def mostra_tela_opcoes(self):
        self.init_components()
        button, value = self.__window.Read()
        switcher = {
            'incluir' : self.inclui,
            'alterar' : self.altera,
            'excluir' : self.exclui
        }
        if button is None:
            return 0, None
        else:
            funcao_escolhida = switcher[button]
            info = funcao_escolhida(value)
            return button, info


    def inclui(self, value):
        try:
            info = {}
            for i in ['cod', 'data', 'jogo', 'num']:
                if value[i] == '':
                    raise CampoVazio()
                else:
                    info[i] = value[i]
            try:
                for i in info['cod']:
                    int(i)
            except ValueError:
                raise CodigoInvalido()
        
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
            self.erro('Numeros Invalidos!')

    def altera(self, value):
        try:
            if value['sorteio-alterar'] == '':
                raise CampoVazio()
            else:
                info = {}
                info['sorteio'] = value['sorteio-alterar']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def exclui(self, value):
        try:
            if len(value['sorteios-excluir']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['sorteios'] = value['sorteios-excluir']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def listagem_sorteio(self, cod, data, jogo, premio, num):
        self.__sorteios.append(cod)
        self.__listagem.append("{} ->  {}  {}  R${:.2f}  {}".format(cod , data.strftime("%d/%m/%Y"),jogo, premio, num))


    def tela_altera(self, cod, data, jogo, num):
        alterar = [
            [sg.Text('Cod:   '), sg.InputText(cod,key="cod", size=(20, 1)),
            sg.Text('Data:   '), sg.InputText(data.strftime("%d/%m/%Y"),key="data", size=(20, 1))],
            [sg.Text('Jogo:'), sg.InputCombo(self.__jogos, jogo,key="jogo", size=(20, 1)),
            sg.Text('Numeros:'), sg.InputText(num, key="num", size=(20, 1))
            ]
        ]
        layout = [
            [sg.Column(alterar),sg.Button("ALTERAR", key="alterar")]
        ]
        self.__window = sg.Window('SORTEIO').Layout(layout)

    def mostra_tela_alterar(self, cod, data, jogo, num):
        self.tela_altera( cod, data, jogo, num)
        button, value = self.__window.Read()
        self.close()
        if button is None:
            return None
        else:
            value['num']= (str(value['num']).replace('(','').replace(')',''))
            infos = self.inclui(value) #valores escritos
            if infos is not None:
                sorteio = [cod, data, jogo, num]
                cont = 0
                infos_novas = {}
                for k,v in infos.items():
                    if v != sorteio[cont]:
                        infos_novas[k] = infos[k]
                    cont +=1
                return infos_novas


    def limpar_listagem(self):
        self.__sorteios = []
        self.__listagem = []

    def close(self):
        self.__window.Close()
    
 