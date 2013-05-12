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

    # kuna sisendis ei ole tegelikult kõik naabrid reale kirjutatud, siis parandame andmeid kontrollides
    # kas iga kvant on iga oma naabri jaoks ka tema naabriks märgitud
    def paranda_kvantide_naabrid(self):
        for kvant in self.kvandid:
            for naabri_nr in kvant.naabrid:
                naaber_kvant = self.kvant_nr(naabri_nr)
                if not kvant.nr in naaber_kvant.naabrid:
                    naaber_kvant.naabrid.append(kvant.nr)

    #maakonnad, linnad on alati rajanud end keskuse äärde, seega mina alustan hoopis suurimatest kvantidest
    def tee_klastrid_peakvandiga(self):
        #self._kvandid_suured_enne = sorted(self.kvandid, key=lambda x: x.kaal, reverse=True)
        self._kvandid_suured_enne = sorted(self.kvandid, key=lambda x: len(x.naabrid), reverse=True)
        # nüüd valin neist välja esimesed m (klastrite arv) kvanti, seega iga klastri "keskuseks" saab üks
        # m suurimaist kvandist
        for i in range(self.klastrite_arv):
            klaster = Klaster()
            klaster.nr = i + 1
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

                if naabri_nr == 1:
                    print "naabri_nr on 1"
                kvant = self.kvant_nr(naabri_nr)
                if kvant:
                    # loodetavasti saab sama naaber teise klastrisse, teise klastri kvandi naabrina ?
                    # ei saagi...
                    if kvant.kaal + klaster.kaal > self.max:
                        print "kvandi %d kaal %d on liiga suur klastri %d jaoks" % (kvant.nr, kvant.kaal, klaster.nr)
                        continue
                    klaster.lisa_kvant(kvant)
                    self.v6etud_kvantide_numbrid.append(kvant.nr)

    # kui mõne klastri miinimum valijate arv pole täis, siis proovi teistest klastritest sinna võtta
    def t2ida_miinimum(self):
        for klaster in self.klastrid:
            self.liiguta_kvant_kui_vaja(klaster)

    # miinimumi täitmiseks
    def liiguta_kvant_kui_vaja(self, klaster):
        if klaster.kaal >= self.min:
            return True

        kaal_puudu = self.min - klaster.kaal
        print "klastris nr %d on liiga v2he, vaja veel %d" % (klaster.nr, kaal_puudu)
        for teine_klaster in self.klastrid:
            if teine_klaster.kaal < self.min:
                continue
                #kui teise klastri kaal on piisavalt suur
            teise_klastri_ylej22k = teine_klaster.kaal - self.min
            print "ülejääk %d" % teise_klastri_ylej22k
            if teise_klastri_ylej22k >= kaal_puudu:
                #kui leiame piisavalt suure ning väikse kaaluga kvandi, siis võtame selle
                for kvant in teine_klaster.kvandid:
                    # siin võiks proovida ka nii et võib mitu kvanti võtta, ehk kvandi kaal ei pea olema
                    #  suurem kui kaal_puudu, aga siis peaks ikkagi eelistama sellist kvanti
                    if kaal_puudu < kvant.kaal < teise_klastri_ylej22k:
                        # kui selle potentsiaalselt sobiva kvandi naabritest mõni on ka selles klastris kuhu meil
                        # teda vaja on (sest ülesanne tahab, et klaster oleks sidus)
                        if set(kvant.kasutatud_naabrite_numbrid) & set(klaster.kvantide_numbrid):
                            print "jah, kvant nr %d,  %s vs %s" % (
                                kvant.nr, kvant.kasutatud_naabrite_numbrid, klaster.kvantide_numbrid)
                            if teine_klaster.eemalda_kvant(kvant):
                                klaster.lisa_kvant(kvant)
                                if klaster.kaal >= self.min:
                                    return True
                                else:
                                    #kui sellest ei piisanud, võta veel kvante
                                    self.liiguta_kvant_kui_vaja(klaster)
        return False

    def v6ta_naaber_kvandi_nr(self, kvant):
        naabri_nr = kvant.v6ta_naabri_nr()
        #kui naaberkvant on juba klastris
        if naabri_nr in self.v6etud_kvantide_numbrid:
            return self.v6ta_naaber_kvandi_nr(kvant)
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
    rahvaloendus.paranda_kvantide_naabrid()
    #print rahvaloendus.kvandid
    #print "------"
    rahvaloendus.tee_klastrid_peakvandiga()
    rahvaloendus.lisa_vaheldumisi_klastritele_kvante()
    rahvaloendus.t2ida_miinimum()

    #rahvaloendus.lisa_kvantide_naabrid_peakvantidele()
    #for klaster in rahvaloendus.klastrid:
    #print klaster.kvandid

    print "kaal peab jääma vahemikku %d-%d" % (rahvaloendus.min, rahvaloendus.max)
    print "kokku peab kvante olema %d" % rahvaloendus.kvantide_arv
    print "kokku peab klastreid olema %d" % rahvaloendus.klastrite_arv

    lahendi_kirjutaja = LahendiKirjutaja()
    lahendi_kirjutaja.kirjuta(rahvaloendus.klastrid)

    v6etud_kvantide_arv = len(rahvaloendus.v6etud_kvantide_numbrid)
    print "Ära võetud %d kvanti: %s" % (v6etud_kvantide_arv, rahvaloendus.v6etud_kvantide_numbrid)

    puuduolevate_kvantide_arv = rahvaloendus.kvantide_arv - v6etud_kvantide_arv
    print "puudu on %d kvanti" % puuduolevate_kvantide_arv