from limite.tela_abstrata import TelaAbstrata

class TelaJogo(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
    
    def mostra_tela_opcoes(self):
        #opcoes tela inicial
        print("---------CADASTRO JOGO---------")
        print("1 - Incluir jogo")
        print("2 - Alterar jogo")
        print("3 - Excluir jogo")
        print("4 - Listar jogo cadastrados")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4])
        return opcao

    def opcoes_alterar(self):
        #opcoes de alteracao do apostador
        print("-----Alterar Jogo------")
        print("1 - Alterar nome")
        print("2 - Alterar maximo de numeros")
        print("3 - Alterar minimo de numeros")
        print("4 - Alterar valor do premio")
        print("0 - Voltar")

        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4])
        return opcao

    def lista_jogo(self, nome: str , max_numeros: int, min_numeros: int, premio: float):
        #imprime dados de cada jogo cadastrado
        print('..........................................')
        print("Nome: {}     Valor premio: R${:.2f}".format(nome, premio))
        print("Max: {} numeros ; Min: {} numeros".format(max_numeros,min_numeros))
        
 