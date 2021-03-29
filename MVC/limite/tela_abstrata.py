from datetime import date

class TelaAbstrata():
    def __init__(self, controlador):
        self.__controlador = controlador

    def  le_opcoes(self, msg: str, inteiros_validos : [] = None):
        while True:
            lido = self.leiaint(msg)
            try:
                if lido not in inteiros_validos:
                    raise ValueError
                return lido
            except ValueError:
                print("Valor incorreto!")
                if inteiros_validos:
                    print("Valores válidos: ", inteiros_validos)

    def leiaint(self, msg: str):
        while True:
            lido = input(msg)
            try:
                num = int(lido)
                return num
            except ValueError:
                print("Digite apenas numeros!")

    def leiaints(self, msg='Digite os números separados por vírgula: '):
        while True:
            lido = input(msg)
            if lido != '':
                lido = lido.split(',')
                lista = []
                try:
                    for num in lido:
                        lista.append(int(num))
                    return lista
                except ValueError:
                    print('Digite apenas números!')

    def pega_dado_str(self,msg: str):
        while True:
            try:
                lido = input(msg)
                if lido != '':
                    return lido
                else:
                    raise ValueError()
            except ValueError:
                print('Valor invalido!')
            

    def pega_dado_int(self, msg: str):
        return self.leiaint(msg)

    def pega_data(self):
        while True:
            try:
                dia = self.pega_dado_int('Dia: ')
                mes = self.pega_dado_int('Mes: ')
                ano = self.pega_dado_int('Ano: ')
                return date(ano, mes, dia)
            except ValueError:
                print('Data invalida!!')

    def msg(self, msg: str):
        print('---------{}---------'.format(msg))

    def lista_apostadores(self, nome: str, cpf: int, idade: int):
        #imprime os dados de cada apostador
        print('__________________________________')
        print("Nome: {}     {} anos    Cpf: {}".format(nome, idade, cpf))
        
 
    def lista_apostas(self, codigo: int, data: date, jogo: str, numeros: list):
        print('__________________________________')
        print("Codigo: {}    {}    Jogo: {}    Numeros apostados: {}".format(codigo, data.strftime("%d/%m/%y"), jogo, numeros)) 

    def lista_sorteio(self, data, jogo, premio, numeros):
        #imprime dados de cada jogo cadastrado
        print('__________________________________')
        print("{}     {} - Valor premio: R${}".format(data.strftime("%d/%m/%y"), jogo,premio))
        print('Numeros sorteados: {}'.format(numeros))
