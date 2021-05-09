from persistencia.abstract_dao import DAO
import pickle as pk

class JogoDAO(DAO):
    def __init__(self):
        super().__init__('jogos.pkl')