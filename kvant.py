class Kvant:
    def __init__(self, nr, kaal, naabrid):
        self.nr = nr
        self.kaal = kaal  # elanike arv
        self.naabrid = naabrid
        self.naabrite_arv = len(naabrid)
        self.komponentide_arv = None
        self.klaster = None