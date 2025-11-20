import copy
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
        self.tour_attrazioni = TourDAO.get_tour_attrazioni()
        # TODO
        for t in self.tour_attrazioni:
            self.tour_map[t["id_tour"]].attrazioni.add(t["id_attrazione"])
            self.attrazioni_map[t["id_attrazione"]].tour.add(t["id_tour"])

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
        self._max_giorni = max_giorni
        self._max_budget = max_budget
        #self._attrazioni_utili =
        #self._tour_utili =


        self._ricorsione(1, [], 0, 0, 0, set())
        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, attrazioni_usate: set):
        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno
        '''
        if valore_corrente > self._valore_ottimo and self._valore_ottimo != -1:
            if (durata_corrente == self._max_giorni or self._max_giorni is None) and (costo_corrente == self._max_budget or self._max_budget is None):
                self._pacchetto_ottimo = copy.deepcopy(pacchetto_parziale)
                self._valore_ottimo = valore_corrente
                print(self._pacchetto_ottimo)
                print(self._valore_ottimo)
        else:

            for t in self.tour_map[start_index]:
                for a in self.attrazioni_map[t.attrazioni]:
                    if a.id not in attrazioni_usate:
                        attrazioni_utili.append(a)
                        attrazioni_usate.add(a.id)
                durata_corrente += t.durata
                costo_corrente += t.costo
                pacchetto_parziale.append((t,attrazioni_utili))
                self._ricorsione(start_index, pacchetto_parziale, durata_corrente, costo_corrente, valore_corrente, attrazioni_usate)
                pacchetto_parziale.pop()
        '''