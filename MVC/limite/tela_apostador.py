from limite.tela_abstrata import TelaAbstrata

class TelaApostador(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostra_tela_opcoes(self):
        #opcoes tela inicial
        print("---------CADASTRO APOSTADOR---------")
        print("1 - Incluir apostador")
        print("2 - Alterar apostador")
        print("3 - Excluir apostador")
        print("4 - Listar apostadores cadastrados")
        print("5 - Listar apostas")
        print("6 - Incluir aposta")
        print("7 - Excluir aposta")
        print("8 - Alterar endereco")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0, 1, 2, 3, 4, 5, 6, 7, 8])
        return opcao

    def opcoes_alterar(self):
        #opcoes de alteracao do apostador
        print("-----Alterar Apostador------")
        print("1 - Alterar nome")
        print("2 - Alterar cpf")
        print("3 - Alterar ano de nascimento")
        print("0 - Voltar")

        opcao = self.le_opcoes("Escolha a opcao: ", [0, 1, 2, 3])
        return opcao