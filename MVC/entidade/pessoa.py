from datetime import date
from abc import ABC, abstractmethod

class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, cpf: str, ano_nascimento: int ):
        self.__nome = nome
        self.__cpf = cpf
        if (date.today().year >= ano_nascimento) and ((date.today().year - ano_nascimento) <= 100):
            self.__ano_nascimento = ano_nascimento
        else:
            raise ValueError()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

    @property
    def ano_nascimento(self):
        return self.__ano_nascimento

    @ano_nascimento.setter
    def ano_nascimento(self, ano_nascimento: int):
        if date.today().year >= ano_nascimento:
            self.__ano_nascimento = ano_nascimento
        else:
            raise ValueError()

    @property
    def idade(self):
        ano_atual = date.today().year
        idade = ano_atual - self.__ano_nascimento
        return idade


