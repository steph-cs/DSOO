class IdadeInvalida(Exception):
    def __init__(self):
        super().__init__('apostador deve ter +18 !!')

class QuantidadeNumerosIncorreta(Exception):
    def __init__(self):
        super().__init__('Quantidade de numeros invalida!!')

class JaExiste(Exception):
    def __init__(self, opcao):
        super().__init__('{} ja existe!!'.format(opcao))

class NaoExiste(Exception):
    def __init__(self, opcao):
        super().__init__('{} não existe!!'.format(opcao))

class ListaVazia(Exception):
    def __init__(self, opcao):
        super().__init__('Lista de {} está vazia!!'.format(opcao))

