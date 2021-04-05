class IdadeInvalida(Exception):
    def __init__(self):
        super().__init__('apostador deve ter +18 !!')

class QuantidadeNumerosIncorreta(Exception):
    def __init__(self):
        super().__init__('Quantidade de numeros invalida!!')
    
class NumerosIncorretos(Exception):
    def __init__(self):
        super().__init__('Escolha numeros entre 1 e 15 e sem repetições!')

class JaExiste(Exception):
    def __init__(self, opcao):
        super().__init__('{} ja existe!!'.format(opcao))

class NaoExiste(Exception):
    def __init__(self, opcao):
        super().__init__('{} não existe!!'.format(opcao))

class ListaVazia(Exception):
    def __init__(self, opcao):
        super().__init__('Lista de {} está vazia!!'.format(opcao))

class CpfQuantidadeIncorreta(Exception):
    def __init__(self):
        super().__init__('Cpf deve conter 14 digitos!')

class CpfFormatoIncorreto(Exception):
    def __init__(self):
        super().__init__('Digite o cpf no formato 000.000.000-00')
