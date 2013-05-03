#!/usr/bin/python
# -*- coding: utf-8 -*-

# kvantide ühendamise programm (klastritesse)

# Lahendiks on tekstifail klastrid.prn: klastri number ja komponentide loetelu
# 1;12,15,7,11,14,16,2,3,4,1;
# 2;13,9,8,5,6,10;

#kvant sisaldab klastreid
from klaster import Klaster
from kvant import Kvant
from lahendi_kirjutaja import LahendiKirjutaja
from sisselugeja import Sisselugeja


class Rahvaloendus:
    def __init__(self):
        # min ja max inimeste arv ühes klastris
        self.min = None
        self.max = None
        self.kvantide_arv = None  # n
        self.klastrite_arv = None  # m
        self.kvandid = []
        self.klastrid = []
        self._kvandid_suured_enne = []
        self.v6etud_kvantide_numbrid = []

    # loeb sisse sisendfailist väärtused ning teeb saadud andmete põhjal
    # vastavad objektid
    def algv22rtusta(self):
        s = Sisselugeja()
        s.loe_sisse()
        self.min = s.min()
        self.max = s.max()
        self.kvantide_arv = s.kvantide_arv()
        self.klastrite_arv = s.klastrite_arv()
        self.kvandid = self._tee_kvandid(s.kvandid())

    #maakonnad, linnad on alati rajanud end keskuse äärde, seega mina alustan hoopis suurimatest kvantidest
    def tee_klastrid_peakvandiga(self):
        self._kvandid_suured_enne = sorted(self.kvandid, key=lambda x: x.kaal, reverse=True)
        # nüüd valin neist välja esimesed m (klastrite arv) kvanti, seega iga klastri "keskuseks" saab üks
        # m suurimaist kvandist
        for i in range(self.klastrite_arv):
            klaster = Klaster()
            kvant = self._kvandid_suured_enne.pop(0)
            klaster.lisa_kvant(kvant)
            self.klastrid.append(klaster)
            self.v6etud_kvantide_numbrid.append(kvant.nr)

    def lisa_vaheldumisi_klastritele_kvante(self):
        i = 0
        while i < 100:
            i += 1
            for klaster in self.klastrid:
                if klaster.kaal >= self.max:
                    continue
                hea_kvant = klaster.leia_hea_kvant()
                if hea_kvant is None:
                    continue
                naabri_nr = self.v6ta_naaber_kvandi_nr(hea_kvant)  # pop
                if naabri_nr is None:
                    #print i
                    continue
                kvant = self.kvant_nr(naabri_nr)
                if kvant:
                    # loodetavasti saab sama naaber teise klastrisse, teise klastri kvandi naabrina ?
                    # ei saagi...
                    if kvant.kaal + klaster.kaal > self.max:
                        continue
                    klaster.lisa_kvant(kvant)
                    self.v6etud_kvantide_numbrid.append(kvant.nr)

    #TODO: fix infinite loophole
    def v6ta_naaber_kvandi_nr(self, kvant):
        naabri_nr = kvant.v6ta_naabri_nr()
        #kui naaberkvant on juba klastris
        if naabri_nr in self.v6etud_kvantide_numbrid:
            self.v6ta_naaber_kvandi_nr(kvant)
        else:
            return naabri_nr

    # tagastab kvandi numbri järgi
    def kvant_nr(self, nr):
        return self.kvandid[nr - 1]

    # teeb sisselugeja kvantide sõnastik-objektidest Kvant objektid
    def _tee_kvandid(self, sisselugeja_kvandid):
        kvandid = []
        for k in sisselugeja_kvandid:
            kvant = Kvant(k['nr'], k['kaal'], k['naabrid'])
            kvandid.append(kvant)
        return kvandid

#kutsutakse välja kui skript pannakse käima käsurealt
if __name__ == "__main__":
    rahvaloendus = Rahvaloendus()
    rahvaloendus.algv22rtusta()
    #print rahvaloendus.kvandid
    #print "------"
    rahvaloendus.tee_klastrid_peakvandiga()
    rahvaloendus.lisa_vaheldumisi_klastritele_kvante()

    #rahvaloendus.lisa_kvantide_naabrid_peakvantidele()
    #for klaster in rahvaloendus.klastrid:
    #print klaster.kvandid

    lahendi_kirjutaja = LahendiKirjutaja()
    lahendi_kirjutaja.kirjuta(rahvaloendus.klastrid)
    print "ok"