import copy
from datetime import time
from functools import lru_cache

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._meteoDao = MeteoDao()
        self._situazioni = self._meteoDao.get_all_situazioni()
        self.costoBest = None
        self.sequenza = []

    def umiditaMediaMese(self, mese):
        umiditaMediaT = 0.0
        umiditaMediaG = 0.0
        umiditaMediaM = 0.0
        giorni = 0
        for situa in self.get_situa_mese(mese):
            giorni += 1
            if situa.localita == "Genova":
                umiditaMediaG += situa.umidita
            elif situa.localita == "Milano":
                umiditaMediaM += situa.umidita
            elif situa.localita == "Torino":
                umiditaMediaT += situa.umidita
        giorni /= 3
        return umiditaMediaG / giorni, umiditaMediaM / giorni, umiditaMediaT / giorni

    def get_situa_mese(self, mese):
        result = []
        for situa in self._situazioni:
            if mese == int(situa.data.strftime("%m")):
                result.append(situa)
        return result

    def get_situa_succ(self, giorno, mese):
        result = []
        for situa in self.get_situa_mese(mese):
            if giorno + 1 == int(situa.data.strftime("%d")):
                result.append(situa)
        return result

    def calcolaSequenza(self, mese):
        self.sequenza = []
        self.costoBest = 7000
        self.ricorsioneSequenza([], mese)
        return self.sequenza, self.costoBest

    def ricorsioneSequenza(self, situazioni, mese):
        if len(situazioni) == 15:
            costo = self.controllaCosto(situazioni)
            if costo < self.costoBest:
                self.costoBest = costo
            self.sequenza = copy.deepcopy(situazioni)
        else:
            for situa in self.get_situa_succ(0 if situazioni == [] else int(situazioni[-1].data.strftime("%d")), mese):
                situazioni.append(situa)
                if self.soddisfaVincoli(situazioni):
                    self.ricorsioneSequenza(situazioni, mese)
                situazioni.pop()

    def controllaCosto(self, seq):
        costo = 0
        for i in range(len(seq)):
            costo += seq[i].umidita
            if i == 0 or i == 1:
                pass
            elif seq[i].localita != seq[i - 1].localita or seq[i].localita != seq[i - 2].localita:
                costo += 100
        return costo

    def soddisfaVincoli(self, seq):
        flag = True
        for i in range(len(seq)):
            if i == 0 or i == 1:
                pass
            elif seq[i].localita != seq[i - 1].localita or seq[i].localita != seq[i - 2].localita:
                flag = False
        return flag
