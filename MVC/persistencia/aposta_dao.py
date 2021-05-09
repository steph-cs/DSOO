from persistencia.abstract_dao import DAO
import pickle as pk

class ApostaDAO(DAO):
    def __init__(self):
        super().__init__('apostas.pkl')