from limite.tela_abstrata import TelaAbstrata

class TelaSistema(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
        self.__controlador = controlador

    def mostra_tela_opcoes(self):
        print("---------LOTERIA---------")
        print("1 - Loteria")
        print("2 - Jogo")
        print("3 - Apostador")
        print("4 - Aposta")
        print("5 - Sorteio")
        print("0 - Sair")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [1, 2, 3, 4, 5, 0])
        return opcao