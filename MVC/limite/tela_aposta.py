from limite.tela_abstrata import TelaAbstrata

class TelaAposta(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostra_tela_opcoes(self):
        #opcoes tela inicial
        print("---------CADASTRO APOSTA---------")
        print("1 - Incluir aposta")
        print("2 - Alterar aposta")
        print("3 - Excluir aposta")
        print("4 - Listar apostas cadastradas")
        print("5 - Listar apostadores")
        print("6 - Incluir apostador")
        print("7 - Excluir apostador")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4,5,6,7])
        return opcao

    def opcoes_alterar(self):
        #opcoes de alteracao do apostador
        print("-----Alterar Aposta------")
        print("1 - Alterar codigo")
        print("2 - Alterar data")
        print("3 - Alterar jogo")
        print("4 - Alterar numeros")
        print("0 - Voltar")

        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4])
        return opcao
    