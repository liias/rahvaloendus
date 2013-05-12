# -*- coding: utf-8 -*-

# Klaster sisaldab Kvante
# kvandid klastris peavad olema sidusad (kvantide naabrite kaudu)
from operator import attrgetter


class Klaster:
    def __init__(self):
        self.nr = None
        self.kaal = 0
        self.kvandid = [] #Kvant objektid

    def lisa_kvant(self, kvant):
        self.kvandid.append(kvant)
        self.kaal += kvant.kaal

    #naabritega tähendab siin, et klastris pole veel kvandil naabrit küljes
    def leia_hea_kvant(self):
        #TODO arvesta kaugus_peakvandist
        #kvant millel on kõige rohkem naabreid juba klastrisse pandud
        a = [x for x in self.kvandid if x.klastrita_naabrite_arv != 0]
        if not a:
            return None


        #    print "klastrita naabrite arv: %d" % k.klastrita_naabrite_arv
        #kvant = min(a)

        kvant = min(a, key=attrgetter('klastrita_naabrite_arv'))

        #võta mingi selle kvandi naaber
        #naabri_nr = self.v6ta_naaber_kvandi_nr(kvant)
        return kvant

    def v2ljund(self):
        return ','.join([str(k.nr) for k in self.kvandid]) + " (%d)" % self.kaal