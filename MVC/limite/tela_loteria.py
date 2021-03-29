from limite.tela_abstrata import TelaAbstrata

class TelaLoteria(TelaAbstrata):
    def __init__(self, controlador):
        super().__init__(controlador)
    
    def mostra_tela_opcoes(self):
        #opcoes tela inicial
        print("---------Loteria---------")
        print("1 - Incluir Aposta")
        print("2 - Excluir Aposta")
        print("3 - Consulta Apostas")
        print("4 - Inclui Sorteio")
        print("5 - Exclui Sorteio")
        print("6 - Consulta Sorteios")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4,5,6])
        return opcao

    def opcoes_consulta_apostas(self):
        #opcoes conculta aposta
        print("---------Consulta Apostas---------")
        print("1 - Lista aposta")
        print("2 - Apostas por jogo")
        print("3 - Apostas por data")
        print("4 - Apostas por jogo e data")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4])
        return opcao

    def opcoes_consulta_sorteios(self):
       #opcoes conculta sorteios
        print("---------Consulta Sorteios---------")
        print("1 - Lista sorteio")
        print("2 - Apostas ganhas")
        print("3 - Ganhadores por jogo")
        print("4 - Ganhadores por data")
        print("5 - Ganhadores por jogo e data")
        print("6 - Ultimas apostas ganhas")
        print("7 - Ultimas apostas ganhas por jogo")
        print("8 - Numeros recorrentes por jogo")
        print("0 - Voltar")
        
        opcao = self.le_opcoes("Escolha a opcao: ", [0,1,2,3,4,5, 6, 7, 8])
        return opcao 

    def lista_ganhadores(self, nome, cpf, idade, data, premio):
        self.lista_apostadores(nome, cpf, idade)
        print('Data da aposta: {}     Premio: R${},00'.format(data, premio))
    
    def numeros_recorrentes(self, num, qnt_vezes):
        print('Numero: {}    {} vezes'.format(num, qnt_vezes))
    