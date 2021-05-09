from entidade.sorteio import Sorteio
from limite.tela_sorteio import TelaSorteio
from datetime import date, timedelta
from entidade.exception import JaExiste, NaoExiste, ListaVazia, QuantidadeNumerosIncorreta, NumerosIncorretos
from persistencia.sorteio_dao import SorteioDAO

class ControladorSorteio():
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_sorteio = TelaSorteio(self)
        self.__dao = SorteioDAO()
    
    def __new__(cls, *args, **kwargs):
        if ControladorSorteio.__instance is None:
            ControladorSorteio.__instance = object.__new__(cls)
        return ControladorSorteio.__instance

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            'incluir' : self.inclui_sorteio,
            'alterar' : self.abre_tela_altera_sorteio,
            'excluir' : self.exclui_sorteio,
        }
        op = True
        while op:
            self.lista_sorteio()

            self.listagem_jogos()

            button, info = self.__tela_sorteio.mostra_tela_opcoes()
            funcao_escolhida = switcher[button]
            if funcao_escolhida is False:
                op = False
            else:
                self.__tela_sorteio.close()
                funcao_escolhida(info)

#listagens
    def listagem(self):
        return self.__tela_sorteio.listagem()

    def listagem_jogos(self):
        control = self.__controlador_sistema.controlador_jogo()
        jogos = list((control.jogos().keys()))
        self.__tela_sorteio.jogos(jogos)

    def sorteios(self):
        return {key: value for key, value in sorted(self.__dao.get_all().items(), key = lambda x: x[1].data)}

    def lista_sorteio(self):
        self.__tela_sorteio.limpar_listagem()
        if len(self.__dao.get_all()) >= 1:
            for i in self.sorteios().values():
                self.__tela_sorteio.listagem_sorteio(i.codigo, i.data, i.jogo.nome,i.jogo.premio, i.numeros)
    
#inclusao/exclusao
    def inclui_sorteio(self, infos: dict):
        if infos is not None:
            codigo = infos['cod']
            try:
                self.__dao.get_all()[codigo] 
            except KeyError:
                try:
                    jogo = self.__controlador_sistema.controlador_jogo().jogos()[infos['jogo']]
                    numeros = infos['num']
                    data = self.__tela_sorteio.data_sorteio(infos['data'])
                    if data is not None:
                        sorteio = Sorteio(codigo, data, jogo, numeros)
                        self.__dao.add(codigo, sorteio)
                        self.__tela_sorteio.erro('Sorteio Adicionado!')
                except KeyError:
                    self.__tela_sorteio.erro('Jogo nao existe!!')
                except QuantidadeNumerosIncorreta as qnt_incorreta:
                    #se qnt de num incorreta mostra o max e min permitido de acordo c o jogo escolhido
                    self.__tela_sorteio.erro(
                    '''{}
                    Min: {}'''.format(qnt_incorreta, jogo.min_numeros))
                except NumerosIncorretos as num_incorretos:
                    self.__tela_sorteio.erro(num_incorretos)    
            else:
                self.__tela_sorteio.erro('Aposta Ja Existe!')

    def exclui_sorteio(self, infos: dict):
        if infos is not None:
            try:
                for sorteio in infos['sorteios']:
                    self.__dao.remove(sorteio.split()[0])
            except KeyError:
                self.__tela_sorteio.erro('Sorteio Nao Existe!')

# acoes altera sorteio

    def abre_tela_altera_sorteio(self, info: dict):
        if info is not None:
            try:
                sorteio = self.__dao.get(info['sorteio'])
                cod = sorteio.codigo
                jogo = sorteio.jogo.nome
                data = sorteio.data
                num = sorteio.numeros
                
                infos = self.__tela_sorteio.mostra_tela_alterar(cod, data, jogo, num)
            
                if infos is not None:
                    switcher = {
                        'cod' : self.altera_codigo,
                        'data' : self.altera_data,
                        'jogo' : self.altera_jogo,
                        'num' : self.altera_numeros
                    }
                    for i in ['cod', 'data', 'jogo', 'num']:
                        if i in infos:
                            switcher[i](sorteio, infos[i])       
            except KeyError:
                self.__tela_aposta.erro('Sorteio nao existe!')
            except QuantidadeNumerosIncorreta as qnt_incorreta:
                self.__tela_sorteio.erro(qnt_incorreta)
            except NumerosIncorretos as num_incorretos:
                self.__tela_sorteio.erro(num_incorretos)
        #opcoes de alteracao do sorteio

    def altera_codigo(self, sorteio, cod):
        try:
            self.__dao.get(cod)
            self.__tela_sorteio.erro('Sorteio ja existe!')
        except KeyError:
            self.__dao.remove(sorteio.codigo)
            sorteio.codigo = cod
            self.__dao.add(cod, sorteio)

    def altera_data(self, sorteio, data):
        #altera data da sorteio
        #pega jogo, data verifica a existencia do sorteio
        data = self.__tela_sorteio.data_sorteio(data)
        if data is not None:
            self.__dao.remove(sorteio.codigo)
            sorteio.data = data
            self.__dao.add(sorteio.codigo, sorteio)

    def altera_jogo(self, sorteio, jogo):
        try:
            jogo = self.__controlador_sistema.controlador_jogo().jogos()[jogo]
            self.__dao.remove(sorteio.codigo)
            sorteio.jogo = jogo
            self.__dao.add(sorteio.codigo, sorteio)
        except KeyError:
            self.__tela_sorteio.erro('Jogo nao existe!!')

    def altera_numeros(self, sorteio, num):
        self.__dao.remove(sorteio.codigo)
        sorteio.numeros = num
        self.__dao.add(sorteio.codigo, sorteio)
