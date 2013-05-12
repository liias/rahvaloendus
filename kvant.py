# -*- coding: utf-8 -*-
class Kvant:
    def __init__(self, nr, kaal, naabrid):
        self.nr = int(nr)
        self.kaal = int(kaal)  # elanike arv
        self.naabrid = naabrid #numbrite list
        #self.naabrite_arv = len(naabrid)
        self.klastrita_naabrite_arv = len(naabrid)
        self.komponentide_arv = None
        self.klaster = None
        self._kasutatud_naabrid = []
        self.kaugus_peakvandist = None

    #võta esimene naaber
    def v6ta_naabri_nr(self):
        if self.nr == 4:
            print "neli"
        if self.klastrita_naabrite_arv == 0:
            return None
        self.klastrita_naabrite_arv -= 1
        naaber = self.naabrid.pop()
        return naaber

    def v6ta_naaber_indeks(self):
        self.klastrita_naabrite_arv -= 1

    def v6ta_naaber_nr(self):
        self.klastrita_naabrite_arv -= 1

    #def v6ta_naaber_nr(self, nr):
    #    self.kasutatud_naabrite_nrid.append(nr)
    #
    #    return self.naabrid.pop(i)

    def __str__(self):
        return "nr: %d, kaal: %d, klaster: %s" % (self.nr, self.kaal, self.klaster)

    # et print kvandid näitaks ilusat teksti
    def __repr__(self):
        return self.__str__()