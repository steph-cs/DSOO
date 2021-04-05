class Endereco:
    def __init__(self, estado: str, cidade: str):
        self.__estado = estado
        self.__cidade = cidade

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado: str):
        self.__estado = estado
    
    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str):
        self.__cidade = cidade