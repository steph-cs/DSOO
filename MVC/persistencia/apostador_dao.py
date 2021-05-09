from persistencia.abstract_dao import DAO
import pickle as pk

class ApostadorDAO(DAO):
    def __init__(self):
        super().__init__('apostadores.pkl')