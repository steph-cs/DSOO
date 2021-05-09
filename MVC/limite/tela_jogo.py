from limite.tela_abstrata import TelaAbstrata
import PySimpleGUI as sg
from entidade.exception import CampoVazio

class TelaJogo(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.__window = None
        self.__listagem = []
        self.__jogos = []

    def init_components(self):
        #opcoes tela inicial
    
        inclusao = [
            [sg.Text('Nome:   '), sg.InputText(key="nome", size=(20, 1)),
            sg.Text('Premio:'), sg.InputText(key="premio", size=(20, 1))],
            [sg.Text('Maximo:'), sg.InputText(key="max", size=(20, 1)),
            sg.Text('Minimo:'), sg.InputText(key="min", size=(20, 1))]
        ]
        layout = [
            [sg.Column(inclusao),sg.Button("INCLUIR", key="incluir")],
            [sg.InputCombo(self.__jogos, size=(20, 1), key='jogo-alterar'), 
            sg.Button("ALTERAR", key="alterar")],
            [sg.Listbox(values=(self.__listagem), select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50,4), key='jogos-excluir'),sg.Button("EXCLUIR", key="excluir")]
        ]
        self.__window = sg.Window('JOGO').Layout(layout)
    
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
            for i in ['nome', 'premio','max', 'min']:
                if value[i] == '':
                    raise CampoVazio()
            info = {}
            info['nome'] = value['nome'].capitalize()
            for i in ['premio','max', 'min']:
                info[i] = int(value[i])
            return info
        except CampoVazio as vazio:
            self.erro(vazio)
        except ValueError:
            self.erro('Numero Invalido!')

    def altera(self, value):
        try:
            if value['jogo-alterar'] == '':
                raise CampoVazio()
            else:
                info = {}
                info['jogo'] = value['jogo-alterar']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)

    def exclui(self, value):
        try:
            if len(value['jogos-excluir']) == 0:
                raise CampoVazio()
            else:
                info = {}
                info['jogos'] = value['jogos-excluir']
                return info
        except CampoVazio as vazio:
            self.erro(vazio)


    def listagem_jogo(self, nome, max, min, premio):
        self.__jogos.append(nome)
        self.__listagem.append("{}   R${:.2f}   Max: {}   Min: {} ".format(nome, premio, max, min))


    def tela_altera(self, nome, premio, max, min):
        alterar = [
            [sg.Text('Nome:   '), sg.InputText(nome,key='nome', size=(20, 1)),
            sg.Text('Premio:'), sg.InputText(premio,key='premio', size=(20, 1))],
            [sg.Text('Maximo:'), sg.InputText(max,key='max', size=(20, 1)),
            sg.Text('Minimo:'), sg.InputText(min,key='min', size=(20, 1))]
        ]
        layout = [
            [sg.Column(alterar),sg.Button("ALTERAR", key="alterar")]
        ]
        self.__window = sg.Window('JOGO').Layout(layout)

    def mostra_tela_alterar(self, nome, premio, max, min):
        self.tela_altera(nome, premio, max, min)
        button, value = self.__window.Read()
        self.close()
        if button is None:
            return None
        else:
            infos = self.inclui(value) #valores escritos
            if infos is not None:
                jogo = [nome, premio, max, min]
                cont = 0
                infos_novas = {}
                for k,v in infos.items():
                    if v != jogo[cont]:
                        infos_novas[k] = infos[k]
                    cont +=1
                return infos_novas


    def limpar_listagem(self):
        self.__jogos = []
        self.__listagem = []

    def close(self):
        self.__window.Close()