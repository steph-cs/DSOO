from limite.tela_abstrata import TelaAbstrata
from datetime import date, timedelta

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

    def data_sorteio(self):
        #pega a data ...
        data = self.pega_data()
        #se for domingo retorna a data..
        if data.weekday() == 6:
            return data
        else:
            #se nao, mostra a data do dom anterior e do prox
            dom_anterior = data
            prox_dom = data
            while prox_dom.weekday() != 6:
                prox_dom = prox_dom + timedelta(days=1)
            while dom_anterior.weekday() != 6:
                dom_anterior = dom_anterior - timedelta(days=1)
            print('Sorteios ocorrem somente aos domingos!')
            print('Dom anterior: ', dom_anterior.strftime("%d/%m/%y"))
            print('Prox dom: ', prox_dom.strftime("%d/%m/%y")) 
 