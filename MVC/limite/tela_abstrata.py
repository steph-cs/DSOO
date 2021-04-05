from datetime import date
from entidade.exception import CpfFormatoIncorreto, CpfQuantidadeIncorreta


class TelaAbstrata():
    def __init__(self, controlador):
        self.__controlador = controlador

    def  le_opcoes(self, msg: str, inteiros_validos : [] = None):
        while True:
            lido = self.le_int(msg)
            try:
                if lido not in inteiros_validos:
                    raise ValueError
                return lido
            except ValueError:
                print("Valor incorreto!")
                if inteiros_validos:
                    print("Valores válidos: ", inteiros_validos)

    def le_int(self, msg: str):
        while True:
            lido = input(msg)
            try:
                num = int(lido)
                return num
            except ValueError:
                print("Digite apenas numeros!")

    def pega_premio(self):
        while True:
            lido = input('Valor do premio: R$')
            try:
                num = float(lido)
                return num
            except ValueError:
                print("Digite apenas numeros!")

    def le_ints(self, msg='Digite os números separados por vírgula: '):
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
                    return lido.capitalize()
                else:
                    raise ValueError()
            except ValueError:
                print('Valor invalido!') 

    def pega_dado_int(self, msg: str):
        return self.le_int(msg)

    def pega_data(self):
        while True:
            try:
                dia = self.pega_dado_int('Dia: ')
                mes = self.pega_dado_int('Mes: ')
                ano = self.pega_dado_int('Ano: ')
                return date(ano, mes, dia)
            except ValueError:
                print('Data invalida!!')

    def pega_datas(self):
        while True:
            try:
                self.msg('Data Minima')
                data_min = self.pega_data()
                self.msg('Data Maxima')
                data_max = self.pega_data()
                if data_max >=  data_min:
                    return {'data_min': data_min, 'data_max':data_max}
                else:
                    raise ValueError()
            except ValueError:
                print('Data maxima deve ser maior ou igual a data minima!')
                
    def pega_cpf(self, msg: str):
        while True:
            cpf = input(msg)
            try:
                if len(cpf) == 14:
                    if (cpf[3] == '.') and (cpf[7] == '.') and (cpf[11] == '-'):
                        int(cpf.replace('.','').replace('-',''))
                        return(cpf)
                    else:
                        raise CpfFormatoIncorreto()
                else:
                    raise CpfQuantidadeIncorreta()
            except CpfFormatoIncorreto as cpf_formato:
                self.msg(cpf_formato)
            except CpfQuantidadeIncorreta as cpf_qnt:
                self.msg(cpf_qnt)

    def msg(self, msg: str):
        print('---------{}---------'.format(msg))

    def lista_apostadores(self, nome: str, cpf: int, idade: int, estado, cidade):
        #imprime os dados de cada apostador
        print('..........................................')
        print("Nome: {}     {} anos    Cpf: {}  {} - {} ".format(nome, idade, cpf, estado, cidade))
 
    def lista_apostas(self, codigo: int, data: date, jogo: str, numeros: list):
        print('..........................................')
        print("Codigo: {}    {}    Jogo: {}    Numeros apostados: {}".format(codigo, data.strftime("%d/%m/%y"), jogo, numeros)) 

    def lista_sorteio(self, data: date, jogo: str, premio: float, numeros: list):
        #imprime dados de cada jogo cadastrado
        print('..........................................')
        print("{}     {} - Valor premio: R${:.2f}".format(data.strftime("%d/%m/%y"), jogo,premio))
        print('Numeros sorteados: {}'.format(numeros))
