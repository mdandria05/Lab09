from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        # TODO: Aggiungere eventuali altri attributi
        self._max_giorni = None
        self._max_budget = None
        self._id_regione = None
        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """
        # TODO
        self.tour_attrazioni = TourDAO.get_tour_attrazioni()
        for t in self.tour_attrazioni:
            self.tour_map[t["id_tour"]].attrazioni.add(self.attrazioni_map[t["id_attrazione"]])
            self.attrazioni_map[t["id_attrazione"]].tour.add(self.tour_map[t["id_tour"]])

    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        # TODO
        self._max_giorni = max_giorni if max_giorni is not None else float("inf")
        self._max_budget = max_budget if max_budget is not None else float("inf")
        self._id_regione = id_regione
        self._ricorsione([], 0, 0, 0, set())
        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, attrazioni_usate: set):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""
        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno
        if durata_corrente > self._max_giorni or costo_corrente > self._max_budget: return
        elif valore_corrente > self._valore_ottimo:
            self._pacchetto_ottimo = list(pacchetto_parziale)
            self._costo = costo_corrente
            self._valore_ottimo = valore_corrente
        for id_tour in self.tour_map:
            if self.tour_map[id_tour].id_regione == self._id_regione:
                if not  self.tour_map[id_tour].attrazioni & attrazioni_usate:
                    pacchetto_parziale.append(self.tour_map[id_tour])
                    attrazioni_usate.update(self.tour_map[id_tour].attrazioni)
                    valore = 0
                    for a in attrazioni_usate:
                        valore += a.valore_culturale
                    self._ricorsione(pacchetto_parziale, durata_corrente+self.tour_map[id_tour].durata_giorni, costo_corrente+self.tour_map[id_tour].costo,valore,set(attrazioni_usate))
                    attrazioni_usate.difference_update(self.tour_map[id_tour].attrazioni)
                    pacchetto_parziale.pop()