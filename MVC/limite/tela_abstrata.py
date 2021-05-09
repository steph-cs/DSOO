
from datetime import date, timedelta
import PySimpleGUI as sg

class TelaAbstrata():
    def __init__(self, controlador):
        self.__controlador = controlador
    
    def verifica_numeros(self, numeros):
        try:
            numeros = numeros.split(',')
            lista = []
            for num in numeros:
                lista.append(int(num))
            return sorted(lista)
        except ValueError:
            self.erro('Numeros separados por virgula!!')      

    def verifica_data(self, data):
        try:
            if len(data) == 10:
                data = data.split('/')
                for i in range(len(data)):
                    data[i] = int(data[i])
                data = date(data[2],data[1],data[0])
                return data
            else:
                raise ValueError()
        except ValueError:
            self.erro('''
            Data invalida!! 
            Formato valido: 00/00/0000''')
       
    def erro(self,msg):
        sg.Popup('Erro',msg)

    def data_sorteio(self, data):
        #se for domingo retorna a data..
        if data.weekday() == 6:
            return data
        else:
            #se nao, mostra a data do dom anterior e do prox
            dom_anterior = data
            prox_dom = data
            while prox_dom.weekday() != 6:
                prox_dom = prox_dom + timedelta(days=1)
            while dom_anterior.weekday() != 6:
                dom_anterior = dom_anterior - timedelta(days=1)
            self.erro(
            '''Sorteios ocorrem somente aos domingos!
            Dom anterior: {}
            Prox dom: {}
            '''.format(dom_anterior.strftime("%d/%m/%y"),prox_dom.strftime("%d/%m/%y")))

    def verifica_data_max_min(self, datas: dict):
        if datas['max'] != '' or datas['min'] != '':
            info= {}
            for i in ['max', 'min']:
                if datas[i] != '':
                    info[i] = self.verifica_data(datas[i])
                else:
                    info[i] = None
            n_vazia = None
            if None in info.values():
                for data in info.values():
                    if data is not None:
                        n_vazia = data
                for i in info.keys():
                    info[i] = n_vazia
            return info   
        else:
            return {'max': None, 'min': None} 
    