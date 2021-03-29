from limite.tela_abstrata import TelaAbstrata

class TelaSorteio(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
    
    def mostra_tela_opcoes(self):
        #opcoes tela inicial
        print("---------CADASTRO JOGO---------")
        print("1 - Incluir sorteio")
        print("2 - Alterar sorteio")
        print("3 - Excluir sorteio")
        print("4 - Listar sorteios cadastrados")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4])
        return opcao

    def opcoes_alterar(self):
        #opcoes de alteracao do apostador
        print("-----Alterar Apostador------")
        print("1 - Alterar data")
        print("2 - Alterar jogo")
        print("3 - Alterar numeros")
        print("0 - Voltar")

        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3])
        return opcao

 