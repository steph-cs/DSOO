
class ControladorAbstrato:
    def __init__(self):
        pass

    def num_rep(self, numeros: list):
        rep = False
        cont = 0
        while rep is False and cont< len(numeros):
            if numeros.count(numeros[cont]) > 1:
                rep = True
            else:
                cont += 1
        return rep