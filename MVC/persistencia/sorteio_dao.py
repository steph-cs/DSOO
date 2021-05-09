from persistencia.abstract_dao import DAO
import pickle as pk

class SorteioDAO(DAO):
    def __init__(self):
        super().__init__('sorteios.pkl')