from limite.tela_jogo import TelaJogo
from entidade.jogo import Jogo
from entidade.exception import JaExiste, NaoExiste, QuantidadeNumerosIncorreta, ListaVazia
from persistencia.jogo_dao import JogoDAO

class ControladorJogo():
    __instance = None

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_jogo = TelaJogo(self)
        self.__dao = JogoDAO()
    
    def __new__(cls, *args, **kwargs):
        if ControladorJogo.__instance is None:
            ControladorJogo.__instance = object.__new__(cls)
        return ControladorJogo.__instance

    def inicia(self):
        #abre tela inicial
        self.abre_tela_inicial()

    def abre_tela_inicial(self):
        #tela inicial
        switcher = {
            0 : False,
            'incluir' : self.inclui_jogo,
            'alterar' : self.abre_tela_altera_jogo,
            'excluir' : self.exclui_jogo
        }
        op = True
        while op:

            self.lista_jogo()
            button, info = self.__tela_jogo.mostra_tela_opcoes()
            funcao_escolhida = switcher[button]
            if funcao_escolhida is False:
                op = False
            else:
                self.__tela_jogo.close()
                funcao_escolhida(info)

    def jogos(self):
        return {key: value for key, value in sorted(self.__dao.get_all().items(), key = lambda x: x[1].nome)}

    def inclui_jogo(self, infos: dict):
        #pega e verifca a nao existencia do jogo..
        if infos is not None:
            nome = infos['nome']
            try:
                existe = self.__dao.get_all()[nome] 
            except KeyError:
                lido = True
                premio = infos['premio']
                try:        
                    #se nao existente pega o resto dos dados
                    max_num = infos['max']
                    min_num = infos['min']
                    #cria e inclui o jogo
                    jogo = Jogo(nome, max_num, min_num, premio)
                    #self.__jogos.append(jogo)
                    self.__dao.add(nome, jogo)
                except QuantidadeNumerosIncorreta as qnt_incorreta:
                    self.__tela_jogo.erro(qnt_incorreta)
            else:
                self.__tela_jogo.erro('Jogo Ja Existe!')

    def exclui_jogo(self, infos: dict):
        #exclui jogo
        #pede o nome do jogo para alterar..
        if infos is not None:
            try:
                for jogo in infos['jogos']:
                    self.__dao.remove(jogo.split()[0])
            except KeyError:
                self.__tela_jogo.erro('Jogo Nao Existe!')

    def lista_jogo(self):
        # lista os jogos
        self.__tela_jogo.limpar_listagem()
        if len(self.__dao.get_all()) >= 1:
            for i in self.jogos().values():
                self.__tela_jogo.listagem_jogo(i.nome, i.max_numeros, i.min_numeros, i.premio)

    #alteracao
    def abre_tela_altera_jogo(self, info: dict):
        #opcoes de alteracao do apostador
        if info is not None:
            try:
                jogo = self.__dao.get(info['jogo'])
                nome = jogo.nome
                premio = jogo.premio
                max = jogo.max_numeros
                min = jogo.min_numeros
                infos = self.__tela_jogo.mostra_tela_alterar(nome, premio, max, min)
                if infos is not None:
                    for i in ['nome', 'premio','max', 'min']:
                        if i in infos:
                            switcher = {
                            'nome' : self.altera_nome,
                            'premio' : self.altera_premio,
                            'max' : self.altera_max,
                            'min' : self.altera_min
                            }
                            switcher[i](jogo, infos[i])       
            except KeyError:
                self.__tela_jogo.erro('Jogo nao existe!')
            except QuantidadeNumerosIncorreta as qnt_incorreta:
                self.__tela_jogo.erro(qnt_incorreta)

    def altera_nome(self, jogo, nome):
        try:
            self.__dao.get(nome)
            self.__tela_jogo.erro('Jogo ja existe!')
        except KeyError:
            self.__dao.remove(jogo.nome)
            jogo.nome = nome
            self.__dao.add(nome, jogo)

    def altera_premio(self, jogo, premio):
        self.__dao.remove(jogo.nome)
        jogo.premio = premio
        self.__dao.add(jogo.nome, jogo)

    def altera_max(self, jogo, max):
        self.__dao.remove(jogo.nome)
        jogo.max_numeros = max
        self.__dao.add(jogo.nome, jogo)

    def altera_min(self, jogo, min):
        self.__dao.remove(jogo.nome)
        jogo.min_numeros = min
        self.__dao.add(jogo.nome, jogo)
