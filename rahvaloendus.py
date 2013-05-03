#!/usr/bin/python
# -*- coding: utf-8 -*-

# kvantide ühendamise programm (klastritesse)

# Lahendiks on tekstifail klastrid.prn: klastri number ja komponentide loetelu
# 1;12,15,7,11,14,16,2,3,4,1;
# 2;13,9,8,5,6,10;

#kvant sisaldab klastreid
from kvant import Kvant
from sisselugeja import Sisselugeja


class Rahvaloendus:
    def __init__(self):
        self.min = None
        self.max = None
        self.kvantide_arv = None  # n
        self.klastrite_arv = None  # m
        self.kvandid = []

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