class IdadeInvalida(Exception):
    def __init__(self):
        super().__init__('apostador deve ter +18 !!')

class AnoInvalido(Exception):
    def __init__(self):
        super().__init__('Ano inserido invalido !!')

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

class CodigoInvalido(Exception):
    def __init__(self):
        super().__init__('Codigo invalido!')

class CampoVazio(Exception):
    def __init__(self):
        super().__init__('Campo(s) Vazio(s)!')
