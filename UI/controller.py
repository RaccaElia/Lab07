import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        mese = int(self._view.dd_mese.value)
        umiditaMedia = self._model.umiditaMediaMese(mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è: "))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {umiditaMedia[2].__round__(2)}"))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {umiditaMedia[1].__round__(2)}"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {umiditaMedia[0].__round__(2)}"))
        self._view.update_page()


    def handle_sequenza(self, e):
        mese = int(self._view.dd_mese.value)
        situazioni = self._model.calcolaSequenza(mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {situazioni[1]}:"))
        for situa in situazioni[0]:
            self._view.lst_result.controls.append(ft.Text(f"{situa.__str__()}"))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

